import os
import sys
import socket
import queue
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from .config import Config


def get_log_level(level_str):
    if level_str == 'info':
        level = logging.INFO
    elif level_str == 'warn':
        level = logging.WARNING
    elif level_str == 'error':
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return level


class AgentLog:
    def __init__(self, agent: str):
        self.agent = agent
        self.log_queue = queue.Queue()
        self.listener = None
        self.logger = None
        self.home = os.getenv('ATHENA_HOME')
        self._init_logger()

    def _init_logger(self):
        # Formatter
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        config = Config('athena-agent.yaml')
        level = get_log_level(config.get_value('log/level'))
        count = self._get_log_count(config.get_value('log/rotate'))
        size = self._get_log_bytes(config.get_value('log/size'))
        name = self._get_log_name()

        # File Handler
        file_handler = RotatingFileHandler(filename=name, maxBytes=size, backupCount=count)
        file_handler.setFormatter(formatter)

        # Queue Listener
        self.listener = logging.handlers.QueueListener(self.log_queue, file_handler)
        self.listener.start()

        # Queue Handler
        queue_handler = logging.handlers.QueueHandler(self.log_queue)

        # Logger
        self.logger = logging.getLogger(self.agent)
        self.logger.setLevel(level)
        self.logger.addHandler(queue_handler)
        self.logger.propagate = False

    def get_logger(self) -> logging.Logger:
        return self.logger

    def close(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _get_log_count(self, rotate_str):
        return int(rotate_str)

    def _get_log_bytes(self, size_str):
        i = size_str.find('kb')
        if i > 0:
            return int(size_str[:i]) * 1024
        i = size_str.find('mb')
        if i > 0:
            return int(size_str[:i]) * 1024 * 1024
        i = size_str.find('gb')
        if i > 0:
            return int(size_str[:i]) * 1024 * 1024 * 1024
        return 0

    def _get_log_name(self):
        path = os.path.join(self.home, 'logs', 'agent')
        os.makedirs(path, exist_ok=True)
        file = self.agent + '@' + socket.gethostname() + '.log'
        return os.path.join(path, file)


class AppLog:
    def __init__(self, app: str, devel=False):
        self.app = app
        self.devel = devel
        self.home = os.getenv('ATHENA_HOME')
        self.logger = self._get_or_create_logger()

    def _get_or_create_logger(self):
        # Formatter
        formatter = logging.Formatter('%(asctime)s %(levelname)s #(%(thread)s) %(message)s')

        if not self.devel:
            logger = logging.getLogger(self.app)
            if not logger.handlers:
                config = Config('athena-app.yaml')
                level = get_log_level(config.get_value('log/level'))
                date_fmt = config.get_value('log/path').strip('{}')
                path = os.path.join(self.home, 'logs', 'app')
                file = self.app + '@' + socket.gethostname() + '.log'

                file_handler = CustomTimedRotatingFileHandler(path, file, date_fmt)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                logger.setLevel(level)
                logger.propagate = False
        else:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, base_dir, filename, date_format, when='midnight', interval=1, backupCount=0):
        self.base_dir = base_dir
        self.date_format = date_format
        self.filename = filename
        self.update_log_dir()
        log_filename = os.path.join(self.log_dir, filename)
        super().__init__(log_filename, when=when, interval=interval, backupCount=backupCount)

    def update_log_dir(self):
        """
        Method to update the log directory based on the current time
        """
        current_time = datetime.now().strftime(self.date_format)
        self.log_dir = os.path.join(self.base_dir, current_time)
        os.makedirs(self.log_dir, exist_ok=True)  # Create directory if it doesn't exist

    def doRollover(self):
        """
        Override the doRollover method to dynamically update the directory and rollover the log file
        """
        # Update the directory and log file path before performing rollover
        self.update_log_dir()

        # Set the new file path in the handler
        self.baseFilename = os.path.join(self.log_dir, self.filename)

        # Call the parent class's rollover function to manage log rotation
        super().doRollover()
