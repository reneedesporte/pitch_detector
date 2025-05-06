"""Module containing classes and methods for the audio data buffer."""

import time
import numpy as np
from collections import deque
from pitch_detector import utils


class Buffer:
    """
    Audio buffer class, which holds and processes audio data.

    NOTE: Only 1-dimensional (single channel) buffer supported
     at this time.

    Attributes
    ----------
    logger : pitch_detector.log.Logger
        Logger for file and terminal.
    sample_rate : int, default=44100
        Audio sample rate.
    data : collections.deque
        Buffer containing audio data.
    ramp_up : int
        Count for initial filling of `data` (buffer).
         Once `ramp_up` is large enough, processing begins.
    """
    def __init__(self, logger, sample_rate=44100):
        """
        Parameters
        ----------
        logger : log.Logger
            Logger for file and terminal.
        sample_rate : int, default=44100
            Audio sample rate.
        """
        self.logger = logger
        self.sample_rate = sample_rate
        self.data = deque(maxlen=sample_rate)
        self.ramp_up = 0

    def alert(self, note, octave):
        """
        Alert user of processing result.

        Parameters
        ----------
        note : str
            The musical note.
        octave : int, str
            The octave to which the musical note belongs.
        """
        self.logger.write(
            f"Octave {octave}: {note}  ", update_position=False
        )
    
    def put(self, array):
        """Insert `array` into `data`."""
        array = array.flatten()
        self.data.extend(array)
        if self.ramp_up < self.sample_rate:
            self.ramp_up += len(array)

    def process(self):
        """Perform signal processing, once ramp up period ends."""
        while True:
            time.sleep(0.5)
            if self.ramp_up >= self.sample_rate:
                self.logger.write("Starting processing!")
                break
        while True:
            data = np.asarray(self.data.copy())
            pitches = utils.extract_pitch(
                data,
                sr=self.sample_rate,
                threshold=2000
            )
            if len(pitches) == 0:
                self.alert("--", "-")
                continue
            note, octave = utils.frequency_to_note(pitches[0])
            self.alert(note, octave)
