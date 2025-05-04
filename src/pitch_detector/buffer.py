"""Module containing classes and methods for the audio data buffer."""

import time
import numpy as np
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
    size : int
        Size of 1-dimensional array (buffer).
    data : ndarray
        Circular buffer containing audio data.
    fill_index : int
        Index at which filling occurs.
    process_index : int
        Index at which processing occurs.
    ramp_up : int
        Count for initial filling of `data` (buffer).
         Once `ramp_up` is large enough, processing begins.
    PROCESSING_SAMPLE_RATE : int, constant
        The number of sample points needed for processing.
         Related to `ramp_up`.
    sample_rate : int, default=44100
        Audio sample rate
    """
    def __init__(self, logger, size=88200, sample_rate=44100):
        """
        Parameters
        ----------
        logger : log.Logger
            Logger for file and terminal.
        size : int, default=88200
            Length of 1-dimensional input data.
        sample_rate : int, default=44100
            Audio sample rate.
        """
        self.logger = logger
        self.size = size
        self.data = np.zeros((size))
        self.fill_index = 0
        self.process_index = 0
        self.ramp_up = 0
        self.PROCESSING_SAMPLE_RATE = (
            44100//2
        )
        self.sample_rate = sample_rate

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
        self.logger.write(f"Octave {octave}: {note}  ", update_position=False)
    
    def put(self, array):
        """Insert `array` into `data`."""
        array = array.flatten()
        for a in array:
            self.fill_index += 1
            if self.fill_index == self.size:
                self.fill_index = 0
            self.data[self.fill_index] = a
        if self.ramp_up < self.size:
            self.ramp_up += len(array)

    def process(self):
        """Perform signal processing, once ramp up period ends."""
        while True:
            time.sleep(0.5)
            if self.ramp_up >= self.PROCESSING_SAMPLE_RATE:
                self.logger.write("Starting processing!")
                break
        while True:
            data = []
            for _ in range(self.PROCESSING_SAMPLE_RATE):
                self.process_index += 1
                if self.process_index == self.size:
                    self.process_index = 0
                data.append(self.data[self.process_index])
            pitches = utils.extract_pitch(
                np.asarray(data),
                self.sample_rate
            )
            if len(pitches) == 0:
                self.alert("--", "-")
                continue
            note, octave = utils.frequency_to_note(pitches[0])
            self.alert(note, octave)
