import time
from logger.status_logger import Color, logger


class TestCodeTwo:
    def __init__(self, pause: int = 5):
        self.pause = pause

    def path_two(self):

        time.sleep(self.pause)
        logger.i_print("path_two", color=Color.RED, inline_print=True)

        for i in range(1, 5):
            time.sleep(self.pause)
            logger.l_print(f"step {i}", color=Color.RED, inline_print=True)
        logger.inline_end()

    def path_three(self):

        time.sleep(self.pause)

        logger.i_print(
            "resetting counter in path_three",
            color=Color.YELLOW,
            counter_reset=True,
            preceding_line=True)

    def path_four(self):

        time.sleep(self.pause)
        logger.i_print(
            "path_four",
            color=Color.BLUE,
            inline_print=True)

        for i in range(1, 5):
            time.sleep(self.pause)
            logger.l_print(f"step {i}", color=Color.BLUE, inline_print=True)
        logger.inline_end()
