import time
from logger.status_logger import Color, logger


class TestCodeTwo:
    def __init__(self, pause: int = 5):
        self.pause = pause

    def path_two(self):

        time.sleep(self.pause)
        logger.i_print("path_two", color=Color.RED)
