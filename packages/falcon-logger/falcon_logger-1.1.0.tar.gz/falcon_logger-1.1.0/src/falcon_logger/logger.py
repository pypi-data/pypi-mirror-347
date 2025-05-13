import copy
import json
import queue
import sys
import threading
import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta


# --------------------
## holds logging functions that replace common python logger functions
class FalconLogger:  # pylint: disable=too-many-public-methods
    ## logging mode with elapsed time and prefixes
    log_mode_elapsed = 1
    ## logging mode with prefixes only
    log_mode_prefix = 2

    # --------------------
    ## constructor
    #
    # @param path        None for stdout, or full path to the logger file
    # @param max_entries (optional) maximum number of entries before a flush is done; default 10
    # @param loop_delay  (optional) time between checking queue; default 0.250 seconds
    def __init__(self, path=None, max_entries=10, loop_delay=0.250):
        ## verbosity; if True print all lines, if not print only errors, excp ad bug lines
        self._verbose = True
        ## the log display mode to use
        self._log_mode = self.log_mode_elapsed

        ## the full path to the log file
        self._path = path

        ## these are used by runner() and need the ability to be saved/restored
        @dataclass
        class RunnerCfg:
            ## the maximum entries to hold in the queue before saving to the file
            max_entries: int
            ## the maximum number of loops before the queue is emptied
            max_count: int
            ## the delay between checking the queue for entries to save
            loop_delay: float

        self._runner_cfg = RunnerCfg(0, 0, 0.0)
        self.set_max_entries(max_entries)
        self.set_loop_delay(loop_delay)
        ## backup of runner_cfg
        self._backup_cfg = copy.deepcopy(self._runner_cfg)

        ## the queue
        self._queue = queue.Queue()
        ## the file pointer
        if self._path is None:
            self._fp = sys.stdout
        else:
            self._fp = open(self._path, 'w', encoding='UTF-8')  # pylint: disable=consider-using-with

        ## flag to the thread to end the loop
        self._finished = False
        ## the thread pointer
        self._thread = threading.Thread(target=self._runner)
        self._thread.daemon = True
        self._thread.start()

        # wait for thread to start
        time.sleep(0.1)

        ## holds the last time a full DTS was written to the log
        self._start_time = 0.0

        ## current number of dots printed
        self._dots = 0
        ## max number of dots to display
        self._max_dots = 3

    # --------------------
    ## set verbosity
    #
    # @param value  (bool) verbosity level
    # @return None
    def set_verbose(self, value):
        self._verbose = value

    # --------------------
    ## set log mode.
    #
    # @param mode  (str) either "elapsed" or "prefix" or throws excp
    # @return None
    def set_mode(self, mode):
        if mode == 'elapsed':
            self._log_mode = self.log_mode_elapsed
        elif mode == 'prefix':
            self._log_mode = self.log_mode_prefix
        else:
            raise Exception(f'Unknown mode: "{mode}", '  # pylint: disable=broad-exception-raised
                            'choose "elapsed" or "prefix"')

    # --------------------
    ## set max entries to allow in the queue before printing them
    #
    # @param value  (int) number of entries; default: 10
    # @return None
    def set_max_entries(self, value):
        self._runner_cfg.max_entries = value
        if self._runner_cfg.max_entries <= 0:
            raise Exception('max_entries must be greater than 0')  # pylint: disable=broad-exception-raised

    # --------------------
    ## set loop delay to check the queue
    #
    # @param loop_delay (float) number of seconds; default: 0.250
    # @return None
    def set_loop_delay(self, loop_delay):
        self._runner_cfg.loop_delay = loop_delay
        if self._runner_cfg.loop_delay < 0.001:
            raise Exception('loop_delay must be >= 0.001 seconds')  # pylint: disable=broad-exception-raised

        # print every loop_delay seconds even if less than max_entries are in the queue
        self._runner_cfg.max_count = int(round(1 / self._runner_cfg.loop_delay, 1))

    # --------------------
    ## set how many dots to print on one line before printing a newline
    #
    # @param value  (int) number of dots
    # @return None
    def set_max_dots(self, value):
        self._max_dots = value
        if self._max_dots <= 0:
            raise Exception('max_dots must be greater than 0')  # pylint: disable=broad-exception-raised

    # === cleanup functions

    # --------------------
    ## terminate
    # stop the thread, save any remaining line in the internal queue
    #
    # @return None
    def term(self):
        self._finished = True
        if self._thread.is_alive():  # pragma: no cover
            # coverage: always taken in tests
            self._thread.join(5)

    # --------------------
    ## do a save at this point
    #
    # @return None
    def save(self):
        self._save()

    # === log lines with prefixes and elapsed times

    # --------------------
    ## add an item to write the full date-time-stamp to the log
    #
    # @return None
    def full_dts(self):
        # the None args/line causes the full dts to display
        self._queue.put((False, self._verbose, time.time(), None, (None,)))

    # --------------------
    ## indicate some activity is starting
    #
    # @param args  the message to log
    # @return None
    def start(self, *args):
        self._queue.put((False, self._verbose, time.time(), '====', args))

    # --------------------
    ## write line with no prefix
    #
    # @param args  the message to log
    # @return None
    def line(self, *args):
        self._queue.put((False, self._verbose, time.time(), '', args))

    # --------------------
    ## write a highlight line
    #
    # @param args  the message to log
    # @return None
    def highlight(self, *args):
        self._queue.put((False, self._verbose, time.time(), '--->', args))

    # --------------------
    ## write an ok line
    #
    # @param args  the message to log
    # @return None
    def ok(self, *args):
        self._queue.put((False, self._verbose, time.time(), 'OK', args))

    # --------------------
    ## write an error line
    #
    # @param args  the message to log
    # @return None
    def err(self, *args):
        self._queue.put((True, self._verbose, time.time(), 'ERR', args))

    # --------------------
    ## write an warn line
    #
    # @param args  the message to log
    # @return None
    def warn(self, *args):
        self._queue.put((False, self._verbose, time.time(), 'WARN', args))

    # --------------------
    ## write a debug line
    #
    # @param args  the message to log
    # @return None
    def bug(self, *args):
        self._queue.put((True, self._verbose, time.time(), 'BUG', args))

    # --------------------
    ## write a debug line
    #
    # @param args  the message to log
    # @return None
    def dbg(self, *args):
        self._queue.put((False, self._verbose, time.time(), 'DBG', args))

    # --------------------
    ## write a raw line (no tag)
    #
    # @param args  the message to log
    # @return None
    def raw(self, *args):
        self._queue.put((False, self._verbose, time.time(), None, args))

    # -------------------
    ## write an output line with the given message
    #
    # @param lineno  (optional) the current line number for each line printed
    # @param args    the message to write
    # @return None
    def output(self, lineno, *args):
        if lineno is None:
            tag = ' --    '
        else:
            tag = f' --{lineno: >3}]'
        self._queue.put((False, self._verbose, time.time(), tag, args))

    # -------------------
    ## write a list of lines using output()
    #
    # @param lines   the lines to write
    # @return None
    def num_output(self, lines):
        lineno = 0
        for line in lines:
            lineno += 1
            self.output(lineno, line)

    # --------------------
    ## if ok is True, write an OK line, otherwise an ERR line.
    #
    # @param ok   condition indicating ok or err
    # @param args  the message to log
    # @return None
    def check(self, ok, *args):
        if ok:
            self.ok(*args)
        else:
            self.err(*args)

    # --------------------
    ## log a series of messages. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param title   the line indicating what the check is about
    # @param lines   individual list of lines to print
    # @return None
    def check_all(self, ok, title, lines):
        self.check(ok, f'{title}: {ok}')
        for line in lines:
            self.check(ok, f'   - {line}')

    # -------------------
    ## add an item to write a 'line' message and a json object to the log
    #
    # @param j       the json object to write
    # @param args    the message to write
    # @return None
    def json(self, j, *args):
        now = time.time()
        self._queue.put((False, self._verbose, now, ' ', args))
        for line in json.dumps(j, indent=2).splitlines():
            self._queue.put((False, self._verbose, now, ' >', (line,)))

    # -------------------
    ## add an item to write a 'line' message and a data buffer to the log in hex
    #
    # @param data    the data buffer to write; can be a string or a bytes array
    # @param args    the message to write
    # @return None
    def hex(self, data, *args):
        now = time.time()
        self._queue.put((False, self._verbose, now, ' ', args))
        i = 0
        line = f'{i:>3} 0x{i:02X}:'
        if isinstance(data, str):
            data = bytes(data, 'utf-8')

        col = 0
        for i, ch in enumerate(data):
            if col >= 16:
                self._queue.put((False, self._verbose, now, '', (' ', line)))
                col = 0
                line = f'{i:>3} 0x{i:02X}:'

            line += f' {ch:02X}'
            col += 1
            if col == 8:
                line += '  '
            # else:
            #     line += ' '

        # print if there's something left over
        self._queue.put((False, self._verbose, now, ' ', (' ', line)))

    # --------------------
    ## write a dot to stdout
    #
    # @return None
    def dot(self):
        self._queue.put((False, self._verbose, time.time(), '.', (None,)))

    # === (some) compatibility with python logger

    # --------------------
    ## log a debug line
    #
    # @param args the line to print; default empty
    # @return None
    def debug(self, *args):
        self._queue.put((False, self._verbose, time.time(), 'DBG', args))

    # --------------------
    ## log an info line
    #
    # @param args the line to print; default empty
    # @return None
    def info(self, *args):
        self._queue.put((False, self._verbose, time.time(), '', args))

    # --------------------
    ## log a warning line
    #
    # @param args the line to print; default empty
    # @return None
    def warning(self, *args):
        self._queue.put((False, self._verbose, time.time(), 'WARN', args))

    # --------------------
    ## log an error line
    #
    # @param args the line to print; default empty
    # @return None
    def error(self, *args):
        self._queue.put((True, self._verbose, time.time(), 'ERR', args))

    # --------------------
    ## log a critical line
    #
    # @param args the line to print; default empty
    # @return None
    def critical(self, *args):
        self._queue.put((True, self._verbose, time.time(), 'CRIT', args))

    # --------------------
    ## log an exception
    #
    # @param excp the exception to print
    # @return None
    def exception(self, excp):
        now = time.time()
        for line in traceback.format_exception(excp):
            for line2 in line.splitlines():
                self._queue.put((True, self._verbose, now, 'EXCP', (line2,)))

    # === logging functions

    # --------------------
    ## save any entries in the queue to the file
    #
    # @return None
    def _save(self):
        if self._fp is None:  # pragma: no cover
            # coverage: can not be replicated
            self._finished = True
            return

        count = self._queue.qsize()
        while count > 0:
            (always_print, verbose, dts, tag, args) = self._queue.get_nowait()
            count -= 1

            if not verbose and not always_print:
                # not verbose and ok not to print
                continue

            # uncomment to debug
            # print(f'{always_print} {verbose} "{tag}"  {dts}  "{line}"')

            if args[0] is None and tag == '.':
                if self._dots == 0:
                    # save delay and count
                    self._backup_cfg = copy.deepcopy(self._runner_cfg)
                    self._runner_cfg.loop_delay = 0.100
                    self._runner_cfg.max_entries = 1
                    self._runner_cfg.max_count = 1

                if self._dots >= self._max_dots:
                    self._fp.write('\n')
                    self._dots = 0

                self._fp.write('.')
                self._dots += 1
                continue

            # at this point, not a dot
            if self._dots != 0:
                self._dots = 0
                self._fp.write('\n')
                self._runner_cfg = copy.deepcopy(self._backup_cfg)

            # print the full DTS requested by the user
            if args[0] is None and tag is None:
                # restart the timer; user wants the full DTS and elapsed is since that absolute time
                self._start_time = dts

                t_str = datetime.fromtimestamp(self._start_time).strftime('%H:%M:%S.%f')[:12]
                dts_str = time.strftime("%Y/%m/%d", time.localtime(self._start_time))
                full_dts = f'{"DTS": <4} {dts_str} {t_str}'
                if self._log_mode == self.log_mode_elapsed:
                    full_dts = f'{"": <6} {full_dts}'
                self._fp.write(full_dts)
                self._fp.write('\n')
                continue

            # print with the prefix, but no elapsed time
            if self._log_mode == self.log_mode_prefix:
                line = ' '.join(map(str, args))
                if tag is None:
                    msg = line
                else:
                    msg = f'{tag:<4} {line}'
                self._fp.write(msg)
                self._fp.write('\n')
                continue

            # at this point, mode is self.LOG_MODE_ELAPSED

            # print prefix and elapsed time
            line = ' '.join(map(str, args))
            elapsed = dts - self._start_time

            # approximately once an hour, restart the time period
            if elapsed > 3600:
                self._start_time = dts

                # print the full DTS; see above
                t_str = datetime.fromtimestamp(self._start_time).strftime('%H:%M:%S.%f')[:12]
                full_dts = f'{"": <6} {"DTS": <4} {time.strftime("%Y/%m/%d", time.localtime(self._start_time))} {t_str}'
                self._fp.write(full_dts)
                self._fp.write('\n')

                # recalc the elapsed time, should be 0
                elapsed = dts - self._start_time

            # log the line
            if tag is None:
                msg = line
            else:
                t_str = timedelta(seconds=elapsed)
                # rare case: str(timedelta) makes the ".000000" optional if the number of microseconds is 0
                if t_str.microseconds == 0:  # pragma: no cover
                    # bump the number of microseconds by 1 to make sure the full string is formatted
                    t_str = timedelta(seconds=elapsed + 0.000001)
                msg = f'{str(t_str)[5:11]} {tag:<4} {line}'

            self._fp.write(msg)
            self._fp.write('\n')

        # flush lines to stdout/file
        self._fp.flush()

    # --------------------
    ## the thread runner
    # wakes periodically to check if the queue has max_entries or more in it
    # if so, the lines are written to the file
    # if not, it sleeps
    #
    # @return None
    def _runner(self):
        count = 0
        while not self._finished:
            # sleep until:
            #  - there are enough entries in the queue
            #  - the max delay is reached
            if self._queue.qsize() < self._runner_cfg.max_entries and count < self._runner_cfg.max_count:
                count += 1
                time.sleep(self._runner_cfg.loop_delay)
                continue

            # write out all the current entries
            count = 0
            self._save()

        # save any remaining entries
        self._save()

        # close the file if necessary
        if self._path and self._fp is not None:  # pragma: no cover
            # coverage: can't be replicated in UTs
            self._fp.close()
            self._fp = None
