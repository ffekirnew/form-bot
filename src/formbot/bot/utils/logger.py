from telebot import logger

logger.setLevel("INFO")


def get_logger():
    return logger
