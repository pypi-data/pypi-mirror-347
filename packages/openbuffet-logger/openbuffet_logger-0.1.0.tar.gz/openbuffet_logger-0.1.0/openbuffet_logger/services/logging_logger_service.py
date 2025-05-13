import logging
import os
from openbuffet_logger.interfaces.ilogger_service import ILoggerService

class LoggingLoggerService(ILoggerService):
    def __init__(self, name="default", log_file_path="logs/app.log"):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

        # Format tanımı
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)

        # Logger'a sadece bir kez handler ekle (çift yazmayı önler)
        if not self._logger.hasHandlers():
            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def debug(self, message: str):
        self._logger.debug(message)
