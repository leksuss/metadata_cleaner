import logging


logging.basicConfig(level=logging.INFO)

error_log_format = logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s')

def error_logger_in_file(name, file='bot_error.log'):
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(error_log_format)
    logger.addHandler(file_handler)
    return logger
