"""Functions to generate and store string artefacts for pipeline log"""
from typing import Type
import re
from connectors import YamlConnector


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
    msg_count : int, optional
        Message counter, by default 0
    mem_msg : str, optional
        String to be kept in "memory" for inline animated progression,
        by default ''
    max_digit : int, optional
        Maximum digits to be expected for counter (determines left white space
        padding), by default 2
    left_offset : int
        The number of white spaces that offset message to the left
    bold : bool, optional
        Whether to display message in bold font, by default False
    color: Type[Color]
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
    inline_sep : str, optional
        Symbol separating messages in inline animation,
        by default '>'
    inline_inplace : bool, optional
        Whether inline messaging overwrites string or is added on to previous
        message, by default False
    inline_color: Type[Color], optional
        Color to display in inline message, by default None

    """

    def __init__(self):

        self.color = Color.BLACK

        params_dict = YamlConnector().get_dict_from_yaml('logger_params.yaml')
        self.msg_count = params_dict['logger']['msg_count']
        self.mem_msg = params_dict['logger']['mem_msg']
        self.max_digit = params_dict['logger']['max_digit']
        self.bold = params_dict['logger']['bold']
        self.left_offset = params_dict['logger']['left_offset']
        self.start_inline = params_dict['logger']['start_inline']
        self.inline_on = params_dict['logger']['inline_on']
        self.preceding_line = params_dict['logger']['preceding_line']

    def _format_text(self, msg: str, bold: bool, color: Type[Color]) -> str:
        if (not bold) & (not color):
            return msg
        else:
            if bold and color:
                return f"{Color.BOLD}{color}{msg}{Color.END}"
            elif bold:
                return f"{Color.BOLD}{msg}{Color.END}"
            elif color:
                return f"{color}{msg}{Color.END}"

    def _log_print(
            self,
            msg: str,
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
        inline_on = kwargs.get('inline_on', self.inline_on)
        start_inline = kwargs.get('start_inline', self.start_inline)
        preceding_line = kwargs.get('preceding_line', self.preceding_line)

        if preceding_line:
            print('')

        if inline_on:
            self.inline_on = False
            print('')

        msg = (" " * left_offset) + msg

        line_output = self._format_text(msg, bold, color)
        self.mem_msg = line_output
        if start_inline:
            self.inline_on = True
            print(f"\r{line_output}", end='', flush=True)
        else:
            print(line_output)

    def l_print(self, msg: str, left_offset: int = None, **kwargs) -> None:
        """Print left offset message in pipeline log"""
        if left_offset is None:
            left_offset = self.max_digit + 2
        self._log_print(msg=msg, left_offset=left_offset, **kwargs)

    def i_print(self, msg: str, counter_reset: bool = False, **kwargs) -> None:
        """Print numerated message in pipeline log"""
        if counter_reset:
            self.msg_count = 1
        else:
            self.msg_count += 1

        msg = f"{self.msg_count:{self.max_digit}}. {msg}"
        self._log_print(msg=msg, **kwargs)

    def _get_len_mem_msg(self):
        """Returns length of self.mem_msg without the color codes"""
        # Regex to match ANSI escape sequences like \x1b[93m or \x1b[0m
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        # Substitute them with an empty string and return the len of text only
        return len(ansi_escape.sub('', self.mem_msg))

    def r_print(
            self,
            msg: str,
            inline_sep: str = ' > ',
            inline_inplace: bool = False,
            msg_pos: int = None,
            **kwargs
            ) -> None:
        """Print inline message in pipeline log"""
        bold = kwargs.get('bold', self.bold)
        color = kwargs.get('color', self.color)

        inline_msg = self._format_text(msg, bold, color)

        if msg_pos is None:
            line_output = f"{self.mem_msg}{inline_sep}{inline_msg}"
        else:
            mem_msg_len = self._get_len_mem_msg()
            if msg_pos > mem_msg_len:
                blnk_multplr = msg_pos - mem_msg_len
            else:
                blnk_multplr = 0

            line_output =\
                f"{self.mem_msg}{' ' * blnk_multplr}{inline_sep}{inline_msg}"

            blnk_multplr = 0

        if inline_inplace is False:
            # Inline message is added onto end of previous inline message
            # (else inline message replaces previous inline message)
            self.mem_msg = line_output

        print(f"\r{line_output}", end='', flush=True)

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
        """
        fill_len = int((header_len - len(header) - 2) / 2)
        msg = "\n" + (fill_symbol*fill_len) + " " + header + " " + (
            fill_symbol*fill_len)
        self._log_print(msg=msg, **kwargs)


logger = Logger()
color = Color()
