"""
Team: MSG - AXIANS

Module that contains logging functions for the project.

This module includes the setup for logging functions for the project. It
includes functions for setting up logging to a file, setting up logging to
the console, and setting up logging to both the console and a file.
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler


class CustomLogger:
    """
    Class that contains logging functions for the project.

    This class includes the setup for logging functions for the entire project. It
    includes functions for setting up logging to a file, setting up logging to
    the console, and setting up logging to both the console and a file.
    """
    def __init__(self, module, log_file='app.log', backup_count=0):
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.INFO)
        # Ensure that handlers are not added multiple times
        if not self.logger.hasHandlers():
            dir_logs = "logs"
            self._set_log_environment(dir_logs, log_file, backup_count)
            

    def _set_log_environment(self, log_name_dir: str, log_name_file: str, backup_count: int):
        """
        Creates a directory and file for logging purposes.

        Args:
            log_name_dir (str): The directory path where the log file will be stored.
            log_name_file (str): The name of the log file.
            backup_count (int): Number of backup files to retain.

        Returns:
            None

        Example:
            set_log_environment("logs", "app.log") 

        This function creates a directory specified by 'log_name_dir' if it doesn't exist 
        and sets up logging to write to a file specified by 'log_name_file' within that directory. 
        If the directory already exists, it will not create a new one.
        """
        file_log = os.path.join(log_name_dir, log_name_file)
        if not os.path.exists(log_name_dir):
            os.makedirs(log_name_dir)

        # An object of the TimedRotatingFileHandler class is instantiated and the input parameters are indicated
        # file_log : file name
        # when: Interval type
        # interval : interval count
        # backupCount : number of backups contemplated in the directory
        handler = TimedRotatingFileHandler(file_log,
                                           when='midnight',
                                           interval=1,
                                           backupCount=backup_count
                                           )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - PID' +
            ': %(process)d(%(threadName)s): %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    def debug(self, message):
        """
        Logs a message at the debug level.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Logs a message at the info level.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Logs a message at the warning level.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Logs a message at the error level.
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Logs a message at the critical level.
        """
        self.logger.critical(message)
