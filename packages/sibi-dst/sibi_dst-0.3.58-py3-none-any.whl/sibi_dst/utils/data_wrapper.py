import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Type, Any, Dict, Optional, Union, List, Tuple
import threading
import fsspec
import pandas as pd
from IPython.display import display
from tqdm import tqdm

from .log_utils import Logger
from .date_utils import FileAgeChecker
from .parquet_saver import ParquetSaver
from .update_planner import UpdatePlanner


class DataWrapper:
    DEFAULT_PRIORITY_MAP = {
        "overwrite": 1,
        "missing_in_history": 2,
        "existing_but_stale": 3,
        "missing_outside_history": 4,
        "file_is_recent": 0
    }
    DEFAULT_MAX_AGE_MINUTES = 1440
    DEFAULT_HISTORY_DAYS_THRESHOLD = 30

    def __init__(self,
                 dataclass: Type,
                 date_field: str,
                 data_path: str,
                 parquet_filename: str,
                 start_date: Any,
                 end_date: Any,
                 fs: Optional[fsspec.AbstractFileSystem] = None,
                 filesystem_type: str = "file",
                 filesystem_options: Optional[Dict] = None,
                 debug: bool = False,
                 verbose: bool = False,
                 class_params: Optional[Dict] = None,
                 load_params: Optional[Dict] = None,
                 reverse_order: bool = False,
                 overwrite: bool = False,
                 ignore_missing: bool = False,
                 logger: Logger = None,
                 max_age_minutes: int = DEFAULT_MAX_AGE_MINUTES,
                 history_days_threshold: int = DEFAULT_HISTORY_DAYS_THRESHOLD,
                 show_progress: bool = False,
                 timeout: float = 60,
                 reference_date: datetime.date = None,
                 custom_priority_map: Dict[str, int] = None,
                 max_threads: int = 3):
        self.dataclass = dataclass
        self.date_field = date_field
        self.data_path = self._ensure_forward_slash(data_path)
        self.parquet_filename = parquet_filename
        self.filesystem_type = filesystem_type
        self.filesystem_options = filesystem_options or {}
        self.fs = fs or self._init_filesystem()
        self.debug = debug
        self.verbose = verbose
        self.class_params = class_params or {}
        self.load_params = load_params or {}
        self.reverse_order = reverse_order
        self.overwrite = overwrite
        self.ignore_missing = ignore_missing
        self.logger = logger or Logger.default_logger(logger_name=self.dataclass.__name__)
        self.logger.set_level(logging.DEBUG if debug else logging.INFO)
        self.max_age_minutes = max_age_minutes
        self.history_days_threshold = history_days_threshold
        self.show_progress = show_progress
        self.timeout = timeout
        self.reference_date = reference_date or datetime.date.today()
        self.priority_map = custom_priority_map or self.DEFAULT_PRIORITY_MAP
        self.max_threads = max_threads

        self.start_date = self._convert_to_date(start_date)
        self.end_date = self._convert_to_date(end_date)
        self._lock = threading.Lock()
        self.processed_dates = []
        self.age_checker = FileAgeChecker(logger=self.logger)

        self.update_planner_params = {
            "data_path": self.data_path,
            "filename": self.parquet_filename,
            "fs": self.fs,
            "debug": self.debug,
            "logger": self.logger,
            "reverse_order": self.reverse_order,
            "overwrite": self.overwrite,
            "ignore_missing": self.ignore_missing,
            "history_days_threshold": history_days_threshold,
            "max_age_minutes": max_age_minutes,
            "show_progress": self.show_progress,
            "description": f"{self.dataclass.__name__}"
        }
        self.update_plan = UpdatePlanner(**self.update_planner_params).generate_plan(self.start_date, self.end_date)


    def _init_filesystem(self) -> fsspec.AbstractFileSystem:
        with self._lock:
            return fsspec.filesystem(self.filesystem_type, **self.filesystem_options)

    @staticmethod
    def _convert_to_date(date: Union[datetime.date, str]) -> datetime.date:
        if isinstance(date, datetime.date):
            return date
        try:
            return pd.to_datetime(date).date()
        except ValueError as e:
            raise ValueError(f"Error converting {date} to datetime: {e}")

    @staticmethod
    def _ensure_forward_slash(path: str) -> str:
        return path.rstrip('/') + '/'

    def generate_date_range(self) -> List[datetime.date]:
        """Generate ordered date range with future date handling"""
        date_range = pd.date_range(
            start=self.start_date,
            end=self.end_date,
            freq='D'
        ).date.tolist()

        if self.reverse_order:
            date_range.reverse()

        return [
            d for d in date_range
            if d <= self.reference_date or self.overwrite
        ]

    def process(self, max_retries: int = 3):
        """Process updates with priority-based execution and retries"""
        #update_plan = self.generate_update_plan()
        update_plan = self.update_plan
        if update_plan.empty:
            self.logger.info("No updates required")
            return
        # Filter for required updates first
        #update_plan = update_plan[update_plan["update_required"] == True]

        if self.show_progress:
            #display(self._enhanced_display_table(update_plan))
            display(update_plan)

        for priority in sorted(update_plan["update_priority"].unique()):
            self._process_priority_group(update_plan, priority, max_retries)

    def _process_priority_group(self,
                                update_plan: pd.DataFrame,
                                priority: int,
                                max_retries: int):
        """Process a single priority group with parallel execution"""
        dates = update_plan[update_plan["update_priority"] == priority]["date"].tolist()
        if not dates:
            return

        desc = f"Processing {self.dataclass.__name__}, task: {self._priority_label(priority)}"
        self.logger.debug(f"Starting {desc.lower()}")
        max_threads = min(len(dates), self.max_threads)
        self.logger.debug(f"DataWrapper Max threads set at: {max_threads}")
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {
                executor.submit(self._process_date_with_retry, date, max_retries): date
                for date in dates
            }

            for future in tqdm(as_completed(futures),
                               total=len(futures),
                               desc=desc,
                               disable=not self.show_progress):
                date = futures[future]
                try:
                    future.result(timeout=self.timeout)
                except Exception as e:
                    self.logger.error(f"Permanent failure processing {date}: {str(e)}")

    def _priority_label(self, priority: int) -> str:
        """Get human-readable label for priority level"""
        return next(
            (k for k, v in self.priority_map.items() if v == priority),
            f"Unknown Priority {priority}"
        )

    def _process_date_with_retry(self, date: datetime.date, max_retries: int):
        """Process a date with retry logic"""
        for attempt in range(1, max_retries + 1):
            try:
                self._process_single_date(date)
                return
            except Exception as e:
                if attempt < max_retries:
                    self.logger.warning(f"Retry {attempt}/{max_retries} for {date}: {str(e)}")
                else:
                    raise RuntimeError(f"Failed processing {date} after {max_retries} attempts") from e

    def _process_single_date(self, date: datetime.date):
        """Core date processing logic"""
        path = f"{self.data_path}{date.year}/{date.month:02d}/{date.day:02d}/"
        full_path = f"{path}{self.parquet_filename}"

        self.logger.info(f"Processing {date} ({full_path})")
        start_time = datetime.datetime.now()

        try:
            self.logger.debug(f"Class Params: {self.class_params}")
            self.logger.debug(f"Load Params: {self.load_params}")

            df = pd.DataFrame()
            with self.dataclass(**self.class_params) as data:
                df = data.load_period(
                    dt_field=self.date_field,
                    start=date,
                    end=date,
                    **self.load_params
                )

            if len(df.index)==0:
                self.logger.warning(f"No data found for {date}")
                return

            with self._lock:
                ParquetSaver(
                    df_result=df,
                    parquet_storage_path=path,
                    fs=self.fs,
                    logger=self.logger
                ).save_to_parquet(self.parquet_filename)

            duration = (datetime.datetime.now() - start_time).total_seconds()
            self._log_success(date, duration, full_path)

        except Exception as e:
            self._log_failure(date, e)
            raise

    def _log_success(self, date: datetime.date, duration: float, path: str):
        """Handle successful processing logging"""
        msg = f"Completed {date} in {duration:.1f}s | Saved to {path}"
        self.logger.info(msg)
        self.processed_dates.append(date)

    def _log_failure(self, date: datetime.date, error: Exception):
        """Handle error logging"""
        msg = f"Failed processing {date}: {str(error)}"
        self.logger.error(msg)


