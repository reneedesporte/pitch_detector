"""Tests for the `utils` module of `pitch_detector`."""

import numpy as np
from pitch_detector import utils

def signal(duration, frequencies, magnitudes=None, sample_rate=44100):
    """
    Generate a signal for test cases.

    Parameters
    ----------
    duration : float
        Duration of sample in seconds.
    frequencies : list
        List of frequencies (Hz).
    magnitudes : list, default=None
        List of magnitudes for each frequency.
            If None, magnitudes will all be 1.
    sample_rate : float, default=44100
        Sample rate.

    Returns
    -------
    ndarray
        Generated signal.
    """
    if magnitudes is None:
        magnitudes = [1] * len(frequencies)

    # Generate sine waves with component frequencies
    t = np.linspace(0, duration, duration*sample_rate)
    y = np.zeros_like(t)
    for freq, mag in zip(frequencies, magnitudes):
        y += mag * np.sin(2 * np.pi * freq * t)

    # Normalize to [-1, 1]
    y -= y.min()
    y /= y.max()
    y -= 0.5
    y *= 2

    return y

def noisify(signal, snr=10):
    """
    Add noise to a signal.
    
    Parameters
    ----------
    signal : ndarray
        The signal which will be made noisy.
    snr : int, default=10
        The signal-to-noise ratio to achieve.
    
    Returns
    -------
    ndarray
        The noisy signal.
    """
    pass

def test_extract_pitch_440():
    """
    Generate a pure sine wave at 440 Hertz, which should be detected
     by `utils.extract_pitch` as the most prominent frequency.
    """
    FREQUENCY = 440  # Hz
    SAMPLE_RATE = 44100  # Hz
    s = signal(1, [FREQUENCY], sample_rate=SAMPLE_RATE)
    pitches = utils.extract_pitch(s, SAMPLE_RATE)
    assert pitches[0] == FREQUENCY
