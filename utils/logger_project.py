import logging


class LoggerProject:
    def get_logger(self) -> logging.Logger:
        # logger = logging.getLogger(__name__)
        logger = logging.getLogger("LoggerProject*****")
        # logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)
        logger.debug('This message should go to the log file')
        logger.info('So should this')
        return logger


my_logger = LoggerProject().get_logger()
