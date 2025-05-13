# openbuffet_logger/interfaces/ilogger_service.py
from abc import ABC, abstractmethod

class ILoggerService(ABC):
    @abstractmethod
    def info(self, message: str): pass

    @abstractmethod
    def warning(self, message: str): pass

    @abstractmethod
    def error(self, message: str): pass

    @abstractmethod
    def debug(self, message: str): pass
