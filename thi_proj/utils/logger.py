import logging
from logging import handlers

# logger名和logger文件存放地址
def get_logger(logger_name, file_path, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        logger.setLevel(level=level)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        # 每天零点存一个文件，最多30个
        time_rotating_file_handler = handlers.TimedRotatingFileHandler(
            file_path, encoding="utf-8", when="MIDNIGHT", interval=1, backupCount=30)
        time_rotating_file_handler.setLevel(level)
        time_rotating_file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        # add handler
        logger.addHandler(time_rotating_file_handler)
        logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger("test", "./test.log")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

    try:
        x = 1 / 0
        logger.info(x)
    except Exception as e:
        logger.error(f"{e}")
