"""Functions to generate and store string artefacts for pipeline log"""
import inspect
from typing import Type

import pandas as pd
import pandasxt as pdx


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
        self.log = self.log + str_output + "\n"

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

    def print_table(
            self,
            dfx: pdx.DataFrameExt,
            bold: bool = False,
            color: Type[Color] = None) -> None:
        """Print data frame as string table

        Parameters
        ----------
        dfx : DataFrameExt
            Data frame
        bold : bool
            Whether to display message in bold font
        Nullcolor: Type[Color]
            Color to display message in; passed on by referencing the class
            'Color', e.g. Color.RED (without quotation marks)
        """
        str_output = dfx.to_str_table(index=False)
        self._log_print(str_output=str_output, bold=bold, color=color)

    def print_count_comparison(
            self,
            dfx1: pdx.DataFrameExt,
            dfx2: pdx.DataFrameExt,
            target_col: str,
            col1_name: str = 'count 1',
            col2_name: str = 'count 2',
            show_total: bool = True,
            return_totals: bool = False) -> None:
        """Compare the value counts of a column from two data frames

        Parameters
        ----------
        dfx1 : DataFrameExt
            First data frame
        dfx2 : DataFrameExt
            Second data frame
        target_col : str
            Column containing the values to be counted
        col1_name : str, optional
            Name of the first count column, by default 'count 1'
        col2_name : str, optional
            Name of the second count column, by default 'count 2'
        show_total : bool, optional
            Flag to indicate whether a total row should be shown,
            by default True
        return_totals : bool, optional
            Flag to indicate whether to return the count totals,
            by default False
        """
        total1 = None
        total2 = None

        df1_count = dfx1.val_count(target_col) \
                        .set_index(target_col) \
                        .rename(columns={'count': col1_name})
        df2_count = dfx2.val_count(target_col) \
                        .set_index(target_col) \
                        .rename(columns={'count': col2_name})

        merged_dfx = df1_count.merge(
            df2_count, on=target_col, how='outer')
        merged_dfx = pdx.DataFrameExt(merged_dfx.reset_index())

        if show_total:
            total1 = df1_count[col1_name].sum()
            total2 = df2_count[col2_name].sum()
            total_row_data = {
                target_col: 'TOTAL',
                col1_name: [total1],
                col2_name: [total2]
            }
            total_row_dfx = pdx.DataFrameExt(total_row_data)
            merged_dfx = pd.concat([merged_dfx, total_row_dfx], axis=0)
            bottom_line_offset = 1
            bottom_line_pattern = '='
        else:
            bottom_line_offset = 0
            bottom_line_pattern = '-'

        merged_dfx = merged_dfx.astype(str)
        merged_dfx[col1_name] = merged_dfx[col1_name].str.replace('.0', '') \
                                                     .str.replace('nan', '-')
        merged_dfx[col2_name] = merged_dfx[col2_name].str.replace('.0', '') \
                                                     .str.replace('nan', '-')
        str_output = merged_dfx.to_str_table(
            bottom_line_offset=bottom_line_offset,
            bottom_line_pattern=bottom_line_pattern,
            left_offset=self.left_offset,
            index=False)

        self._log_print(str_output=str_output, bold=False, color=None)

        if return_totals:
            return total1, total2

    def print_qc_dfx_check(self, **kwargs):

        # Retrieve data frame(s)
        if 'dfx1' in kwargs.keys():
            if isinstance(kwargs['dfx1'], tuple):
                name1 = kwargs['dfx1'][0]
                dfx1 = kwargs['dfx1'][1]
                col1 = kwargs['dfx1'][2]
            else:
                raise TypeError("Pass dfx1 as Tuple, (name1, dfx1) or " +
                                "(name1, dfx1, col1)")
        else:
            raise ValueError("kwargs must specify at least one data frame")

        if 'dfx2' in kwargs.keys():
            if isinstance(kwargs['dfx2'], tuple):
                name2 = kwargs['dfx2'][0]
                dfx2 = kwargs['dfx2'][1]
                col2 = kwargs['dfx2'][2]
            else:
                raise TypeError("Pass dfx2 as Tuple, (name2, dfx2) or " +
                                "(name2, dfx2, col2)")
        else:
            dfx2 = None

        if 'dfx3' in kwargs.keys():
            if isinstance(kwargs['dfx3'], tuple):
                name3 = kwargs['dfx3'][0]
                dfx3 = kwargs['dfx3'][1]
            else:
                raise TypeError("Pass dfx3 as Tuple, (name3, dfx3")
        else:
            dfx3 = None

        # Apply QC check function
        if 'fct' in kwargs.keys():
            # isunique
            if kwargs['fct'] == 'isunique':
                len_dfx1 = len(dfx1)
                val_cnt1 = dfx1[col1].nunique()
                if dfx1.isunique(col1):
                    msg = f"[OK] Column {col1} in {name1} is unique " +\
                          f"- {len_dfx1} values/rows"
                else:
                    msg = f"[! ] Column {col1} in {name1} is not unique: " +\
                          f"{len_dfx1} vs {val_cnt1}!"

            # same_row_count
            if kwargs['fct'] == 'same_row_count':
                len_dfx1 = len(dfx1)
                len_dfx2 = len(dfx2)
                if pdx.same_row_count(dfx1, dfx2):
                    msg = f"[OK] Tables {name1} and {name2} have same row " +\
                          f"count - {len_dfx1} values/rows"
                else:
                    msg = f"[! ] Tables {name1} and {name2} do not have " +\
                          f"same row count - {len_dfx1} vs {len_dfx2}"

            # same_unique_values
            if kwargs['fct'] == 'same_unique_values':
                val_cnt1 = dfx1[col1].nunique()
                val_cnt2 = dfx1[col2].nunique()
                if pdx.same_unique_values((dfx1, col1), (dfx2, col2)):
                    msg = f"[OK] Columns {name1}.{col1} and {name2}.{col2} " +\
                          f"have same unique count - {val_cnt1} values/rows"
                else:
                    msg = f"[! ] Columns {name1}.{col1} and {name2}.{col2} " +\
                          f"do not have same unique count - {val_cnt1} vs " +\
                          f"{val_cnt2}"

            # same_uniq_val_count_as_splits
            if kwargs['fct'] == 'same_uniq_val_count_as_splits':
                val_cnt1 = dfx1[col1].nunique()
                val_cnt2 = dfx2[col2].nunique()
                val_cnt3 = dfx3[col2].nunique()
                if pdx.same_uniq_val_count_as_splits(
                        (dfx1, col1), (dfx2, dfx3, col2)):
                    msg = f"[OK] Column {name1}.{col1} has the same unique " +\
                          f"value count as {name2}.{col2} and {name3}.{col2}" +\
                          f": {val_cnt1} = {val_cnt2} + {val_cnt3}"
                else:
                    msg = f"[! ] Column {name1}.{col1} does not have the " +\
                          f"same value count as {name2}.{col2} " +\
                          f"and {name3}.{col2}: {val_cnt1} = {val_cnt2} + " +\
                          f"{val_cnt3}"

            if msg[:4] == "[OK]":
                color = Color.GREEN
            else:
                color = Color.RED

            # Print message
            self.l_print(msg=msg, color=color)

        else:
            raise ValueError("kwargs must specify a function")

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
