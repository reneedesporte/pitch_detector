"""Module containing classes and methods for logging."""

import os
import curses
from datetime import datetime


class Logger:
    """
    The Logger class handles terminal outputs and logging those
     to file.
    
    NOTE: Upon completion of logging activities, restore
     the terminal to its original state with the `shutdown`
     method.
    
    Attributes
    ----------
    filename : str
        The logfile.
    stdscr : curses.window
        Window object, handling terminal output.
    lock : bool
        Boolean to control class behavior after `shutdown`.
    """
    def __init__(self, savedir=None):
        """
        Parameters
        ----------
        savedir : str or pathlike, default=None
            Save directory

        Raises
        ------
        AssertionError
            If the save directory does not exist.
        """
        if savedir is None:
            savedir = os.getcwd()
        assert os.path.exists(savedir), (
            "Save directory does not exist: "
            f"`{savedir}`"
        )
        self.filename = os.path.join(savedir, "log.txt")
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(f"{datetime.now()}\n")
        
        self.stdscr = curses.initscr()
        curses.noecho()
        self.stdscr.keypad(True)

        self.lock = False

    def write(self, line):
        """
        Write `line` to terminal and file.

        Parameters
        ----------
        line : str
            The line which will be written.

        Returns
        -------
        None
        """
        if self.lock:
            raise RuntimeError(
                "`Logger` instance has been `shutdown`. No logging allowed."
            )
        assert isinstance(line, str), (
            f"`line` must be a string but is of type `{type(line)}`."
        )

        self.stdscr.addstr(10, 10, line)   # TODO provide some other position (10, 10)
        self.stdscr.refresh()
        curses.reset_shell_mode()
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{line}\n")

    def shutdown(self):
        """Return the terminal window to normal on shutdown."""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        print(f"Completed logging to `{self.filename}`")
        self.lock = True
