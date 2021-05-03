# coding=utf-8
import logging
import time
import os
log_path = './log'
class Log:
    def __init__(self):
        self.now = time.strftime("%Y-%m-%d--%H-%M-%S")
        self.logname = os.path.join(log_path, '{0}.log'.format(self.now))
    def __printconsole(self, level, message):
        # create logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # create handler to write log files
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        # create another handler to write console interface
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # define output format of handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)
        logger.addHandler(ch)
        # log
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        # remove handler after logging
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        # cloase file
        fh.close()
    def debug(self, message):
        self.__printconsole('debug', message)
    def info(self, message):
        self.__printconsole('info', message)
    def warning(self, message):
        self.__printconsole('warning', message)
    def error(self, message):
        self.__printconsole('error', message)