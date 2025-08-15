import logging
import sys
from colorama import Fore, Style, init

init(autoreset=True)  # Reset colors automatically after each log line

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

class Logger:
    @staticmethod
    def get_logger(name: str, level=logging.DEBUG):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = ColorFormatter(
                "[%(asctime)s] "
                "[%(name)s] "
                "[%(module)s.%(funcName)s:%(lineno)d] "
                "[%(levelname)s] "
                "%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger


# test logger:
if __name__ == "__main__":
    log = Logger("MyApp").get_logger()

    def sample_function():
        log.debug("Debugging something...")
        log.info("This is an info message")
        log.warning("This is a warning")
        log.error("An error occurred")
        log.critical("Critical failure!")

    sample_function()
