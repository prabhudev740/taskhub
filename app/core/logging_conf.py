from logging import getLogger, StreamHandler, FileHandler, Formatter

_FORMATTER = Formatter(
    fmt="{asctime} - {levelname} - {filename}:{lineno} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class Logging:
    def __init__(self, name):
        self.__name = name

    def log(self):
        logger = getLogger(self.__name)

        console_handler = StreamHandler()
        file_handler = FileHandler("execution.log", mode="a", encoding="utf-8")

        file_handler.setFormatter(_FORMATTER)
        console_handler.setFormatter(_FORMATTER)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(level="DEBUG")

        return logger


if __name__ == "__main__":
    Logging.log().info("This is the logger file")