"""Functions to generate and store string artefacts for pipeline log"""
import inspect
from typing import Type


class Color:
    """Color codes for formatting displayed strings
    """
    BLACK = '\033[30m'
    DARKRED = '\033[31m'
    DARKGREEN = '\033[32m'
    DARKYELLOW = '\033[33m'
    DARKBLUE = '\033[34m'
    PURPLE = '\033[35m'
    DARKCYAN = '\033[36m'
    GRAY = '\033[37m'
    DARKGRAY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Logger:
    """Numerated pipeline logging message

    Atributes
    ---------
    msg_count : int
        Message counter
    log : str
        Log string as shown in terminal
    max_digit : int
        Maximum digits to be expected for counter (determines left white space
        padding)
    left_offset : int
        The number of white spaces that offset message to the left
    """
    def __init__(self):
        self.msg_count = 0
        self.log = ''
        self.max_digit = 2
        self.left_offset = self.max_digit + 2

    def _log_print(
            self,
            str_output: str,
            bold: bool,
            color: Type[Color],
            left_offset: int = 0):
        """Log and print string

        Parameters
        ----------
        str_output : str
            String message to be logged and printed
        bold : bool
            Whether to display message in bold font
        Nullcolor: Type[Color]
            Color to display message in; passed on by referencing the class
            'Color', e.g. Color.RED (without quotation marks)
        left_offset : int, optional
            White space offset from left, by default 0
        """

        str_output = (" " * left_offset) + str_output
        # self.log = self.log + str_output + "\n"

        if (not bold) & (not color):
            print(str_output)
        else:
            if bold and color:
                print(f"{Color.BOLD}{color}{str_output}{Color.END}")
            elif bold:
                print(f"{Color.BOLD}{str_output}{Color.END}")
            elif color:
                print(f"{color}{str_output}{Color.END}")

    def l_print(self,
                msg: str,
                bold: bool = False,
                color: Type[Color] = None) -> None:
        """Print left offset message in pipeline log"""
        self._log_print(str_output=msg, left_offset=self.left_offset,
                        bold=bold, color=color)

    def i_print(self,
                msg: str,
                bold: bool = False,
                color: Type[Color] = None) -> None:
        """Print numerated message in pipeline log"""
        self.msg_count += 1
        str_output = f"{self.msg_count:{self.max_digit}}. {msg}"
        self._log_print(str_output=str_output, bold=bold, color=color)

    def gen_log_header(
            self,
            header: str,
            fill_symbol: str = '*',
            header_len: int = 80,
            bold: bool = False,
            color: Type[Color] = None) -> None:
        """Print a header centered within a header banner of fill symbold

        Parameters
        ----------
        header : str
            Header message to display
        fill_symbol : str, optional
            Symbol to fill the header banner, by default '*'
        header_len : int, optional
            Length of the header banner, by default 80
        bold : bool
            Whether to display message in bold font
        Nullcolor: Type[Color]
            Color to display message in; passed on by referencing the class
            'Color', e.g. Color.RED (without quotation marks)
        """
        fill_len = int((header_len - len(header) - 2) / 2)
        str_output = "\n" + (fill_symbol*fill_len) + " " + header + " " + (
            fill_symbol*fill_len)
        self._log_print(str_output=str_output, bold=bold, color=color)

    @staticmethod
    def get_obj_name(obj: object) -> str:
        """Extract the name of an object"""
        frame = inspect.currentframe().f_back
        for name, value in frame.f_locals.items():
            if value is obj:
                obj_name = name
                break
        if not obj_name:
            raise ValueError("Could not determine the name of the object.")
        return obj_name


logger = Logger()
color = Color()
