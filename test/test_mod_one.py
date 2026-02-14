import time

from test_mod_two import TestCodeRed

from logger.status_logger import Color, logger


class TestCodeBlue:
    def __init__(self, pause: int = 5):
        self.pause = pause

    def _helper_fct(self):
        time.sleep(self.pause)
        logger.i_print("_helper_fct", color=Color.GREEN)

    def path_one(self):

        logger.gen_log_header(
            header="START PROCESS",
            fill_symbol="#",
            color=Color.PURPLE,
        )

        time.sleep(self.pause)
        logger.i_print("path_one", color=Color.BLUE)

        self._helper_fct()

        t_two = TestCodeRed(pause=self.pause)

        t_two.path_two()
        t_two.path_three()
        t_two.path_four()

        logger.gen_log_header(
            header="END PROCESS",
            fill_symbol="#",
            color=Color.PURPLE,
        )
