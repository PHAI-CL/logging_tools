"""Functions to generate and store string artefacts for pipeline log"""
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
    mem_msg : str
        String to be kept in "memory" for inline animated progression
    max_digit : int
        Maximum digits to be expected for counter (determines left white space
        padding)
    left_offset : int
        The number of white spaces that offset message to the left
    bold : bool
        Whether to display message in bold font
    Nullcolor: Type[Color]
        Color to display message in; passed on by referencing the class
        'Color', e.g. Color.RED (without quotation marks)
    left_offset : int, optional
        White space offset from left, by default 0
    preceding_line : bool, optional
        Message is preceded by a blank line, by default False
    inline_print : bool, optional
        Message is printed "inline", i.e. to animate within a line,
        by default False
    inline_reset : bool, optional
        Inline print is reset, i.e., a new animation starts,
        by default False
    """

    def __init__(self):

        self.msg_count = 0
        self.mem_msg = ''
        self.max_digit = 2

        self.bold: bool = False
        self.color: Type[Color] = Color.BLACK
        self.left_offset: int = 0
        self.preceding_line: bool = False
        self.inline_print: bool = False
        self.inline_reset: bool = False

    def _log_print(
            self,
            line_output: str,
            **kwargs
            ):
        """Log and print string

        Parameters
        ----------
        line_output : str
            String message to be logged and printed
        """

        bold = kwargs.get('bold', self.bold)
        color = kwargs.get('color', self.color)
        left_offset = kwargs.get('left_offset', self.left_offset)
        preceding_line = kwargs.get('preceding_line', self.preceding_line)
        inline_print = kwargs.get('inline_print', self.inline_print)
        inline_reset = kwargs.get('inline_reset', self.inline_reset)

        if preceding_line:
            print('')

        line_output = (" " * left_offset) + line_output

        if inline_print:
            if inline_reset or self.mem_msg == '':
                self.mem_msg = line_output
            else:
                self.mem_msg = f"{self.mem_msg} > {line_output}"

            if (not bold) & (not color):
                print(f"\r{self.mem_msg}", end='', flush=True)
            else:
                if bold and color:
                    print(f"\r{Color.BOLD}{color}{self.mem_msg}{Color.END}",
                          end='', flush=True)
                elif bold:
                    print(f"\r{Color.BOLD}{self.mem_msg}{Color.END}",
                          end='', flush=True)
                elif color:
                    print(f"\r{color}{self.mem_msg}{Color.END}",
                          end='', flush=True)
        else:
            if (not bold) & (not color):
                print(line_output)
            else:
                if bold and color:
                    print(f"{Color.BOLD}{color}{line_output}{Color.END}")
                elif bold:
                    print(f"{Color.BOLD}{line_output}{Color.END}")
                elif color:
                    print(f"{color}{line_output}{Color.END}")

    def l_print(self, msg: str, **kwargs) -> None:
        """Print left offset message in pipeline log"""
        left_offset = self.max_digit + 2
        self._log_print(line_output=msg, left_offset=left_offset, **kwargs)

    def i_print(self, msg: str, counter_reset: bool = False, **kwargs) -> None:
        """Print numerated message in pipeline log"""
        if counter_reset:
            self.msg_count = 1
        else:
            self.msg_count += 1

        line_output = f"{self.msg_count:{self.max_digit}}. {msg}"
        self._log_print(line_output=line_output, **kwargs)

    def inline_end(self):
        self._log_print(
            line_output='', preceding_line=True, inline_print=True,
            inline_reset=True)

    def gen_log_header(
            self,
            header: str,
            fill_symbol: str = '*',
            header_len: int = 80,
            **kwargs) -> None:
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
        preceding_line : bool, optional
            Message is preceded by a blank line, by default 0
        """
        fill_len = int((header_len - len(header) - 2) / 2)
        line_output = "\n" + (fill_symbol*fill_len) + " " + header + " " + (
            fill_symbol*fill_len)
        self._log_print(line_output=line_output, **kwargs)


logger = Logger()
color = Color()
