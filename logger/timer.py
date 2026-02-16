""" Modulae for time related functions"""
import time
from datetime import timedelta


class Timer:
    """Numerated pipeline logging message

    Atributes
    ---------
    start_time : time
        time.time() value of instantiation of Timer object.
    total_count : int
        Total number of iterations.
    index_start : int, optional
        Number at which index counter starts, by default 0

    """

    def __init__(
            self,
            total_count: int,
            index_start: int = 0
            ) -> None:
        self.start_time = time.time()
        self.total_count = total_count
        self.index_start = index_start

    def get_est_remaining(self, iter_completed: int) -> str:
        """Return estimated time remaining based on average time per iteration.

        Parameters
        ----------
        iter_completed : int
            The index of the current completed loop iteration.

        Returns
        -------
        str
            Estimated remaining time formatted as HH:MM:SS string.
        """

        # Calculate progress
        iter_remaining = self.total_count - iter_completed

        # Avoid division by zero if total_count is 0
        if iter_completed == self.index_start:
            return "--:--:--"

        # Calculate average time and estimate remaining seconds
        elapsed_time = time.time() - self.start_time
        avg_time_per_iter = elapsed_time / iter_completed
        est_seconds_remaining = avg_time_per_iter * iter_remaining

        # Format to HH:MM:SS using timedelta
        # round() removes microsecond decimals for a cleaner string
        est_delta = timedelta(seconds=round(est_seconds_remaining))
        time_str = str(est_delta)

        # Adjust for timedelta's default H:MM:SS if hours < 10
        if len(time_str) == 7:
            time_str = "0" + time_str

        return time_str
