"""Module containing classes and methods for logging."""

import os
import curses
from collections import deque
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
    y : int
        Y-axis position on screen
    notes : collections.deque
        Small buffer for ever-accumulating musical notes,
         to ensure logfile doesn't get too big.
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
        self.y = 0
        self.notes = deque(maxlen=1000)

    def write(self, line, update_position=True):
        """
        Write `line` to terminal and file.

        Parameters
        ----------
        line : str
            The line which will be written.
        update_position : boolean, default=True
            If True, the y-axis position of the outputted
             text will be updated. 
            Should be set to False when frequently / continuously
             updating the same line.

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

        self.stdscr.addstr(self.y, 10, line)
        self.stdscr.refresh()
        curses.reset_shell_mode()

        if update_position:
            self.y += 1
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"{line}\n")
            return

        self.notes.append(f"{line}\n")

    def shutdown(self):
        """Return the terminal window to normal on shutdown."""
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

        with open(self.filename, "a", encoding="utf-8") as f:
            for note in self.notes:
                f.write(note)

        print(f"Completed logging to `{self.filename}`")
        self.lock = True
