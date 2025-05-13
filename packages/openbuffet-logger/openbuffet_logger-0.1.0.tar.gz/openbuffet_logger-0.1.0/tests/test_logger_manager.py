import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from openbuffet_logger.logger_manager import LoggerManager
from openbuffet_logger.interfaces.ilogger_service import ILoggerService

class MockLogger(ILoggerService):
    def __init__(self):
        self.calls = []

    def info(self, message: str): self.calls.append(("info", message))
    def warning(self, message: str): self.calls.append(("warning", message))
    def error(self, message: str): self.calls.append(("error", message))
    def debug(self, message: str): self.calls.append(("debug", message))

class TestLoggerManager(unittest.TestCase):
    def test_logging(self):
        mock = MockLogger()
        manager = LoggerManager(mock)
        manager.info("info")
        manager.error("error")
        self.assertIn(("info", "info"), mock.calls)
        self.assertIn(("error", "error"), mock.calls)

if __name__ == "__main__":
    unittest.main()
