import logging
import asyncio
from logging import getLogger, StreamHandler, FileHandler, Formatter
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from ..utils import utils

# Initialize colorama for Windows compatibility
init(autoreset=True)


class AsyncFileHandler(FileHandler):
    def __init__(self, filename):
        super().__init__(filename)
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor()

    async def emit(self, record):
        msg = self.format(record)
        await self.loop.run_in_executor(self.executor, self._write, msg)

    def _write(self, msg):
        with self._open() as file:
            file.write(f"{msg}\n")
            file.flush()


class ColorFormatter(Formatter):
    """Custom formatter to add colors depending on the log level."""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE + Style.BRIGHT,
        logging.INFO: Fore.GREEN + Style.BRIGHT,
        logging.ERROR: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Apply color based on the log level
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE + Style.NORMAL)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


class AsyncLogger:
    _instance = None  # Class-level variable to hold singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AsyncLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, name, file_path=None):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent re-initialization
        self._initialized = True

        self.logger = getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Set formatter for the logs with colors
        formatter = ColorFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console Handler with color support
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File Handler (Asynchronous)
        if file_path:
            async_file_handler = AsyncFileHandler(file_path)
            async_file_handler.setFormatter(
                Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            )  # No color for file
            self.logger.addHandler(async_file_handler)

    async def info(self, message):
        await self._log_async(self.logger.info, message)

    async def error(self, message):
        await self._log_async(self.logger.error, message)

    async def debug(self, message):
        await self._log_async(self.logger.debug, message)

    async def _log_async(self, log_func, message):
        await asyncio.get_event_loop().run_in_executor(None, log_func, message)


class LoggerWrapper:
    _instance = None  # Class-level variable to hold singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerWrapper, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger: AsyncLogger):
        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent re-initialization
        self._initialized = True

        self.logger = logger
        self.loop = utils.get_event_loop()
        asyncio.set_event_loop(self.loop)

    def info(self, message):
        self.loop.run_until_complete(self.logger.info(message))

    def error(self, message):
        self.loop.run_until_complete(self.logger.error(message))

    def debug(self, message):
        self.loop.run_until_complete(self.logger.debug(message))


# Exposing the logger as a singleton instance
logger_instance = AsyncLogger(name="graph_ml", file_path="graph_ml.log")
logger = LoggerWrapper(logger_instance)
