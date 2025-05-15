import asyncio
import logging
import datetime
import psutil
import time
from functools import total_ordering
from collections import defaultdict
from contextlib import asynccontextmanager
import signal
from sibi_dst.utils import Logger

@total_ordering
class PrioritizedItem:
    def __init__(self, priority, artifact):
        self.priority = priority
        self.artifact = artifact

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

class ArtifactUpdaterMultiWrapper:
    def __init__(self, wrapped_classes=None, debug=False, **kwargs):
        self.wrapped_classes = wrapped_classes or {}
        self.debug = debug
        self.logger = kwargs.setdefault(
            'logger', Logger.default_logger(logger_name=self.__class__.__name__)
        )
        self.logger.set_level(logging.DEBUG if debug else logging.INFO)

        today = datetime.datetime.today()
        self.parquet_start_date = kwargs.get(
            'parquet_start_date',
            datetime.date(today.year, 1, 1).strftime('%Y-%m-%d')
        )
        self.parquet_end_date = kwargs.get(
            'parquet_end_date',
            today.strftime('%Y-%m-%d')
        )

        # track pending/completed/failed artifacts
        self.pending = set()
        self.completed = set()
        self.failed = set()

        # concurrency primitives
        self.locks = {}
        self.locks_lock = asyncio.Lock()
        self.worker_heartbeat = defaultdict(float)
        self.workers_lock = asyncio.Lock()

        # dynamic scaling config
        self.min_workers = kwargs.get('min_workers', 1)
        self.max_workers = kwargs.get('max_workers', 3)
        self.memory_per_worker_gb = kwargs.get('memory_per_worker_gb', 1)
        self.monitor_interval = kwargs.get('monitor_interval', 10)
        self.retry_attempts = kwargs.get('retry_attempts', 3)
        self.update_timeout_seconds = kwargs.get('update_timeout_seconds', 600)
        self.lock_acquire_timeout_seconds = kwargs.get('lock_acquire_timeout_seconds', 10)

    async def get_lock_for_artifact(self, artifact):
        key = artifact.__class__.__name__
        async with self.locks_lock:
            if key not in self.locks:
                self.locks[key] = asyncio.Lock()
            return self.locks[key]

    def get_artifacts(self, data_type):
        if data_type not in self.wrapped_classes:
            raise ValueError(f"Unsupported data type: {data_type}")
        artifacts = [cls(
            parquet_start_date=self.parquet_start_date,
            parquet_end_date=self.parquet_end_date,
            logger=self.logger,
            debug=self.debug
        ) for cls in self.wrapped_classes[data_type]]
        # seed pending set and clear others
        self.pending = set(artifacts)
        self.completed.clear()
        self.failed.clear()
        return artifacts

    def estimate_complexity(self, artifact):
        try:
            return artifact.get_size_estimate()
        except Exception:
            return 1

    def prioritize_tasks(self, artifacts):
        queue = asyncio.PriorityQueue()
        for art in artifacts:
            queue.put_nowait(PrioritizedItem(self.estimate_complexity(art), art))
        return queue

    async def resource_monitor(self, queue, workers):
        while not queue.empty():
            try:
                avail = psutil.virtual_memory().available
                max_by_mem = avail // (self.memory_per_worker_gb * 2**30)
                optimal = max(self.min_workers,
                              min(psutil.cpu_count(), max_by_mem, self.max_workers))
                async with self.workers_lock:
                    current = len(workers)
                    if optimal > current:
                        for _ in range(optimal - current):
                            wid = len(workers)
                            workers.append(asyncio.create_task(self.worker(queue, wid)))
                            self.logger.info(f"Added worker {wid}")
                    elif optimal < current:
                        for _ in range(current - optimal):
                            w = workers.pop()
                            w.cancel()
                            self.logger.info("Removed a worker")
                await asyncio.sleep(self.monitor_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Monitor error: {e}")
                await asyncio.sleep(self.monitor_interval)

    @asynccontextmanager
    async def artifact_lock(self, artifact):
        lock = await self.get_lock_for_artifact(artifact)
        try:
            await asyncio.wait_for(lock.acquire(), timeout=self.lock_acquire_timeout_seconds)
            yield
        finally:
            if lock.locked():
                lock.release()

    async def async_update_artifact(self, artifact, **kwargs):
        for attempt in range(1, self.retry_attempts + 1):
            lock = await self.get_lock_for_artifact(artifact)
            try:
                await asyncio.wait_for(lock.acquire(), timeout=self.lock_acquire_timeout_seconds)
                try:
                    self.logger.info(f"Updating {artifact.__class__.__name__} (attempt {attempt})")
                    await asyncio.wait_for(
                        asyncio.to_thread(artifact.update_parquet, **kwargs),
                        timeout=self.update_timeout_seconds
                    )
                    # mark success
                    async with self.workers_lock:
                        self.pending.discard(artifact)
                        self.completed.add(artifact)
                    self.logger.info(
                        f"✅ {artifact.__class__.__name__} done — "
                        f"{len(self.completed)}/{len(self.completed) + len(self.pending) + len(self.failed)} completed, "
                        f"{len(self.failed)} failed"
                    )
                    return
                finally:
                    if lock.locked():
                        lock.release()
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout on {artifact.__class__.__name__}, attempt {attempt}")
            except Exception as e:
                self.logger.error(f"Error on {artifact}: {e}")
            finally:
                if lock.locked():
                    lock.release()
            await asyncio.sleep(2 ** (attempt - 1))

        # all retries exhausted -> mark failure
        async with self.workers_lock:
            self.pending.discard(artifact)
            self.failed.add(artifact)
        self.logger.error(f"✖️  Permanently failed {artifact.__class__.__name__}")

    async def worker(self, queue, worker_id, **kwargs):
        while True:
            try:
                item = await queue.get()
                art = item.artifact
                self.worker_heartbeat[worker_id] = time.time()
                await self.async_update_artifact(art, **kwargs)
            except asyncio.CancelledError:
                self.logger.info(f"Worker {worker_id} stopped")
                break
            finally:
                queue.task_done()

    def calculate_initial_workers(self, count: int) -> int:
        avail = psutil.virtual_memory().available
        max_by_mem = avail // (self.memory_per_worker_gb * 2**30)
        return max(self.min_workers,
                   min(psutil.cpu_count(), max_by_mem, count, self.max_workers))

    async def update_data(self, data_type, **kwargs):
        self.logger.info(f"Starting update for {data_type}")
        artifacts = self.get_artifacts(data_type)
        queue = self.prioritize_tasks(artifacts)
        init = self.calculate_initial_workers(len(artifacts))
        tasks = [asyncio.create_task(self.worker(queue, i, **kwargs)) for i in range(init)]
        monitor = asyncio.create_task(self.resource_monitor(queue, tasks))
        await queue.join()
        monitor.cancel()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self.logger.info(self.format_results_table())
        self.logger.info("All artifacts processed.")

    def format_results_table(self):
        results = self.get_update_status()
        headers = ["Metric", "Value"]
        rows = [
            ["Total", results['total']],
            ["Completed", results['completed']],
            ["Pending", results['pending']],
            ["Failed", results['failed']],
            ["Pending Items", len(results['pending_items'])],
            ["Failed Items", len(results['failed_items'])]
        ]

        # Find max lengths for alignment
        max_metric = max(len(str(row[0])) for row in rows)
        max_value = max(len(str(row[1])) for row in rows)

        format_str = "{:<%d}  {:>%d}" % (max_metric, max_value)

        table = [
            "\n",
            format_str.format(*headers),
            "-" * (max_metric + max_value + 2)
        ]

        for row in rows:
            table.append(format_str.format(row[0], row[1]))

        return "\n".join(table)

    def get_update_status(self):
        total = len(self.pending) + len(self.completed) + len(self.failed)
        return {
            "total": total,
            "completed": len(self.completed),
            "pending": len(self.pending),
            "failed": len(self.failed),
            "pending_items": [a.__class__.__name__ for a in self.pending],
            "failed_items": [a.__class__.__name__ for a in self.failed]
        }

# Top‑level driver
# environment = None  # fill this in with your wrapped_classes dict
#
# async def main():
#     wrapper = ArtifactUpdaterMultiWrapper(
#         wrapped_classes=environment,
#         debug=True
#     )
#     loop = asyncio.get_running_loop()
#     for sig in (signal.SIGINT, signal.SIGTERM):
#         loop.add_signal_handler(sig, lambda: asyncio.create_task(wrapper.shutdown()))
#     await wrapper.update_data("your_data_type")
#
# if __name__ == "__main__":
#     asyncio.run(main())

