# openbuffet_logger/logger_manager.py
from openbuffet_logger.interfaces.ilogger_service import ILoggerService

class LoggerManager:
    def __init__(self, logger_service: ILoggerService):
        self._logger = logger_service

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def debug(self, message: str):
        self._logger.debug(message)
