import os
from dataclasses import dataclass
import logging


class CustomFilter(logging.Filter):
    COLOR = {
        "DEBUG": "GREEN",
        "INFO": "GREEN",
        "WARNING": "YELLOW",
        "ERROR": "RED",
        "CRITICAL": "RED",
    }

    def filter(self, record):
        record.color = CustomFilter.COLOR[record.levelname]
        return True


@dataclass
class BaseLogger:
    _log_formats = {
        'minimum': '[%(levelname)s] | %(message)s',
        'normal': '%(asctime)s [%(levelname)s] %(name)s -| %(message)s',
        'detailed': '%(asctime)s [%(levelname)s] | %(name)s.%(funcName)s -| %(message)s',
    }
    _log_format = ''

    _log_levels = {
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'critical': logging.CRITICAL,
        'fatal': logging.FATAL
    }

    def get_file_handler(self, process_name):
        if not os.path.exists('./logs'):
            os.mkdir('logs')

        file_handler = logging.FileHandler(f"./logs/{process_name}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(self._log_format))
        return file_handler

    def get_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(logging.Formatter(self._log_format))
        return stream_handler

    def get_logger(self,
                   process_name,
                   log_level='debug',
                   log_format='normal',
                   file_handler=False,
                   stream_handler=True,
                   filter=False):
        logger = logging.getLogger(process_name)

        # set log lvl
        if log_level not in self._log_levels:
            logging.warning("Invalid log_level -> log_level = [debug]")
            log_level = 'debug'

        logger.setLevel(self._log_levels[log_level])

        # set log format:
        if log_format not in self._log_formats:
            logging.warning("Invalid log_format -> self.log_format = [normal]")
            log_format = 'normal'

        self._log_format = self._log_formats[log_format]

        if file_handler:
            logger.addHandler(self.get_file_handler(process_name))

        if stream_handler:
            logger.addHandler(self.get_stream_handler())

        if filter:
            logger.addFilter(CustomFilter())

        return logger
