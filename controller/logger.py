import sys
import logging
import logging.config

LEVELS = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}


class MyLogger:
    loggers = set()

    def __init__(self, name, level='INFO', log_format="%(asctime)s | %(name)-50s | %(levelname)-8s | %(message)s"):
        self.format = log_format
        self.level = level
        self.name = name
        self.console_formatter = logging.Formatter(self.format)
        self.console_logger = logging.StreamHandler(sys.stdout)
        self.console_logger.setFormatter(self.console_formatter)
        self.logger = logging.getLogger(name)
        if name not in self.loggers:
            self.loggers.add(name)
            self.logger.setLevel(self.level)
            self.logger.addHandler(self.console_logger)

    def _log(self, msg: str, level: str, marker: str = None):
        if marker:
            getattr(self.logger, level)(f'{3 * marker} {msg} {3 * marker}')
        else:
            getattr(self.logger, level)(msg)

    def info(self, msg, **kwargs):
        return self._log(msg, 'info', **kwargs)

    def error(self, msg, **kwargs):
        return self._log(msg, 'error', **kwargs)

    def debug(self, msg, **kwargs):
        return self._log(msg, 'debug', **kwargs)

    def warning(self, msg, **kwargs):
        return self._log(msg, 'warning', **kwargs)
