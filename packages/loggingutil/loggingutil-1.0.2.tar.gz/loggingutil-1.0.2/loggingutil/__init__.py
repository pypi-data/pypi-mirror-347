import os
import gzip
import json
import asyncio
import traceback
from datetime import datetime, timedelta
from typing import Union, Callable, Optional

class LogFile:
    """Creates the LogFile object for logging. (eg. logs = loggingutil.LogFile(...))"""
    def __init__(self,
                 filename: str = "logs.log",
                 verbose: bool = True,
                 max_size_mb: int = 5,
                 keep_days: int = 7,
                 timestamp_format: str = "[%Y-%m-%d %H:%M:%S]",
                 mode: str = "text",
                 compress: bool = False,
                 use_utc: bool = False,
                 include_timestamp: bool = True,
                 custom_formatter: Optional[Callable] = None,
                 external_stream: Optional[Callable[[str], None]] = None):
        self.filename = filename
        self.verbose = verbose
        self.max_size = max_size_mb * 1024 * 1024
        self.keep_days = keep_days
        self.timestamp_format = timestamp_format
        self.mode = mode.lower()
        self.compress = compress
        self.use_utc = use_utc
        self.include_timestamp = include_timestamp
        self.custom_formatter = custom_formatter
        self.external_stream = external_stream
        self.buffer = []
        self.buffer_limit = 5

        self.loadfile()
        self.cleanup_old_logs()

    def _print(self, msg):
        if self.verbose:
            print(f"LoggingUtility :: {msg}")

    def loadfile(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("LoggingUtility::LOGFILE_INIT\n")
            self._print(f"Created new log file: {self.filename}")

    def _rotate_if_needed(self):
        if os.path.exists(self.filename) and os.path.getsize(self.filename) >= self.max_size:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S') if self.use_utc else datetime.now().strftime('%Y%m%d_%H%M%S')
            base, ext = os.path.splitext(self.filename)
            rotated_name = f"{base}_{timestamp}{ext}.gz" if self.compress else f"{base}_{timestamp}{ext}"
            with open(self.filename, 'rb') as f_in:
                with gzip.open(rotated_name, 'wb') if self.compress else open(rotated_name, 'wb') as f_out:
                    f_out.write(f_in.read())
            os.remove(self.filename)
            self._print(f"Log rotated: {rotated_name}")

    def cleanup_old_logs(self):
        base, _ = os.path.splitext(self.filename)
        now = datetime.utcnow() if self.use_utc else datetime.now()
        for file in os.listdir("."):
            if file.startswith(base + "_"):
                try:
                    timestamp_str = file.split("_")[-1].split(".")[0]
                    file_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    if now - file_time > timedelta(days=self.keep_days):
                        os.remove(file)
                        self._print(f"Deleted old log file: {file}")
                except Exception:
                    continue

    def _get_timestamp(self):
        now = datetime.utcnow() if self.use_utc else datetime.now()
        return now.strftime(self.timestamp_format) if self.include_timestamp else ""

    def _format_entry(self, data, level, tag):
        if self.custom_formatter:
            return self.custom_formatter(data, level, tag)
        timestamp = self._get_timestamp()
        level_tag = f"[{level.upper()}]"
        tag_part = f"[{tag}]" if tag else ""
        if self.mode == "json":
            return json.dumps({
                "timestamp": timestamp,
                "level": level.upper(),
                "tag": tag,
                "data": data
            }) + "\n"
        else:
            return f"{timestamp} {level_tag} {tag_part} {data}\n"

    def _write(self, entry: str):
        self._rotate_if_needed()
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(entry)
        if self.external_stream:
            self.external_stream(entry.strip())

    def log(self, data, level="INFO", tag=None):
        if not data:
            return "No data provided"
        entry = self._format_entry(data, level, tag)
        self.buffer.append(entry)
        if len(self.buffer) >= self.buffer_limit:
            self.flush()

    def flush(self):
        for entry in self.buffer:
            self._write(entry)
        self.buffer.clear()
        self._print("Buffer flushed to file.")

    async def async_log(self, data, level="INFO", tag=None):
        self.log(data, level, tag)

    async def async_log_http_response(self, resp, level="INFO", tag="HTTP"):
        try:
            info = {
                "status": resp.status,
                "headers": dict(resp.headers),
                "body": await resp.text()
            }
            self.log(info, level=level, tag=tag)
        except Exception as e:
            self.log_exception(e)

    def log_exception(self, err, tag="EXCEPTION"):
        tb = traceback.format_exc()
        data = {"error": str(err), "traceback": tb}
        self.log(data, level="ERROR", tag=tag)

    def wipe(self):
        with open(self.filename, 'w'):
            pass
        self._print(f"File {self.filename} has been wiped.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
        if exc_type:
            self.log_exception(exc_val)