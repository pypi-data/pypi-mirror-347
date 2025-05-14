import time
import os
import numpy as np
import math as m

# FIXME: Time remaining toggles on/off as list is shortened.
# FIXME: ANSI commands to return to previous line does not work in Powershell/CMD

ANSI_ENDLINE = "\r\x1b[1A"
WIN_ENDLINE = ""

# TODO: Bug testing, iter_list jumped in value
# TODO: Add test with perfomance metrics for different methods and list lengths
ITER_LIST_FLAG = 0
ITER_LIST_MAX_LENGTH = 1_000


class LoopProgress:
    def __init__(self, *loop_iterators, screen_width=None):
        if screen_width is None:
            screen_width = int(os.get_terminal_size().columns - 20)
        self._parse_loop_iterators(loop_iterators)
        self.current_iteration = 0
        self.screen_width = screen_width
        self.start_time = time.time()
        self.iter_duration_list = []
        self.iter_start_time = time.time()

        self.iter_list_length = ITER_LIST_MAX_LENGTH
        if 0.1 * self.N_iterations < ITER_LIST_MAX_LENGTH:
            self.iter_list_length = int(0.1 * self.N_iterations)
        self.iter_list_crop = int(0.05 * ITER_LIST_MAX_LENGTH)
        if 0.005 * self.N_iterations < 0.05 * ITER_LIST_MAX_LENGTH:
            self.iter_list_crop = int(0.005 * self.N_iterations)

        print("Loop initalized.")

    def _parse_loop_iterators(self, loop_iterators):
        self.N_iterations = 1
        for loop in loop_iterators:
            if type(loop) == int:
                self.N_iterations *= len(range(loop))
            else:
                self.N_iterations *= len(loop)

    def return_fraction_complete(self):
        return self.current_iteration / self.N_iterations

    def _update_iter_duration_list(self):
        if not ITER_LIST_FLAG:
            return None
        self.iter_duration_list.append(time.time() - self.iter_start_time)
        self.iter_start_time = time.time()
        if len(self.iter_duration_list) > self.iter_list_length:
            sorted_iter_list = np.sort(self.iter_duration_list)
            self.iter_duration_list = list(
                sorted_iter_list[self.iter_list_crop : -self.iter_list_crop]
            )

    def loop_end(self):
        self.current_iteration += 1
        self._update_iter_duration_list()
        N_hash = int(np.floor(self.return_fraction_complete() * self.screen_width))
        remainder = int(
            np.floor(
                10 * (self.return_fraction_complete() * self.screen_width - N_hash)
            )
        )
        N_spaces = self.screen_width - N_hash

        time_remaining_str = self._time_remaining_str()
        print(
            "|"
            + "#" * N_hash
            + f"{remainder}"
            + " " * (N_spaces)
            + "|"
            + time_remaining_str,
            end="\r",
        )

    def _return_second(self, time):
        return m.floor(time) % 60

    def _return_minute(self, time, include_hours=False):
        minutes = m.floor(time / 60)
        if include_hours:
            return minutes
        return minutes % 60

    def _return_hour(self, time):
        return m.floor(time / 60 / 60)

    def _time_format_str(self, time):
        if self._return_minute(time, include_hours=True) <= 90:
            return f"{self._return_minute(time, include_hours=True):2d}m {self._return_second(time):2d}s"
        elif self._return_hour(time) < 99:
            return f"{self._return_hour(time):2d}h {self._return_minute(time):2d}m"
        else:
            print("Note: Time value is over 99 hours.")
            return f"{self._return_hour(time):d}h {self._return_minute(time):2d}m"

    def _compute_time_per_iter(self):
        if ITER_LIST_FLAG:
            return np.mean(self.iter_duration_list)
        return self._return_elapsed_time() / self.current_iteration

    def _return_time_remaining(self):
        time_per_iter = self._compute_time_per_iter()
        time_remaining = time_per_iter * (self.N_iterations - self.current_iteration)
        return time_remaining

    def _time_remaining_valid_bool(self):
        if ITER_LIST_FLAG:
            if len(self.iter_duration_list) > 0.1 * self.iter_list_length:
                return 1
        elif self.return_fraction_complete() > 0.01 or self._return_elapsed_time() > 10:
            return 1
        return 0

    def _time_remaining_str(self):
        if self._time_remaining_valid_bool():
            return self._time_format_str(self._return_time_remaining())
        return "--m --s"

    def _return_elapsed_time(self):
        return time.time() - self.start_time

    def _time_elapsed_str(self):
        return self._time_format_str(self._return_elapsed_time())

    def print_elapsed_time(self):
        print(f"\nTime Elapsed: {self._time_elapsed_str()}.")
