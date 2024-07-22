"""Module containing the data collection and processing functionality."""

from enum import IntEnum
import scipy
import numpy as np
import sounddevice as sd

class MusicalNotes(IntEnum):
    """
    Musical notes in Hz.

    See Also
    --------
    https://mixbutton.com/mixing-articles/music-note-to-frequency-chart/
    """
    C = [16.35, 32.70, 65.41, 130.81, 261.63, 523.25, 1046.50, 2093.00, 4186.01]
    C_SHARP = [17.32, 34.65, 69.30, 138.59, 277.18, 554.37, 1108.73, 2217.46, 4434.92]
    D = [18.35, 36.71, 73.42, 146.83, 293.66, 587.33, 1174.66, 2349.32, 4698.63]
    D_SHARP = [19.45, 38.89, 77.78, 155.56, 311.13, 622.25, 1244.51, 2489.02, 4978.03]
    E = [20.60, 41.20, 82.41, 164.81, 329.63, 659.25, 1318.51, 2637.02, 5274.04]
    F = [21.83, 43.65, 87.31, 174.61, 349.23, 698.46, 1396.91, 2793.83, 5587.65]
    F_SHARP = [23.12, 46.25, 92.50, 185, 369.99, 739.99, 1479.98, 2959.96, 5919.91]
    G = [24.50, 49, 98, 196, 392, 783.99, 1567.98, 3135.96, 6271.93]
    G_SHARP = [25.96, 51.91, 103.83, 207.65, 415.30, 830.61, 1661.22, 3322.44, 6644.88]
    A = [27.50, 55, 110, 220, 440, 880, 1760, 3520, 7040]
    A_SHARP = [29.14, 58.27, 116.54, 233.08, 466.16, 932.33, 1864.66, 3729.31, 7458.62]
    B = [30.87, 61.74, 123.47, 246.94, 493.88, 932.33, 1975.53, 3951.07, 7902.13]

def record(duration, sr=44100):
    """Record `duration` seconds of audio data from the default microphone.
    
    Parameters
    ----------
    duration : int
        Seconds of data to record.
    sr : int, default=44100
        Sample rate per second.
    
    Returns
    -------
    ndarray
        1-d ndarray of length `duration`*`sr`.
    """
    print("recording!")
    data = sd.rec(duration*sr, samplerate=sr, channels=1)
    sd.wait()
    print("done!")
    return data.flatten()

def extract_pitch(data, sr=44100):
    """Take `data` and apply an FFT to extract prominent
     frequencies on the loudest portion.
    
    Parameters
    -----------
    data : ndarray
        The single-channel audio data.
    sr : int, default=44100
        Sample rate of `data`.
    
    Returns
    --------
    array
        The 1-d array of prominent freqencies in `data`,
         calculated with `scipy.signal.find_peaks`.
    
    See Also
    --------
    scipy.fft.fft
    scipy.fft.fftfreq
    scipy.signal.find_peaks
    """
    # TODO: assert that `data` is the correct shape.

    # Do FFT
    N = len(data)
    T = 1.0 / sr
    yf = scipy.fft.fft(data, axis=0)
    yf = 2.0/N * np.abs(yf[0:N//2]).flatten()  # We only care about positive freqs.
    xf = scipy.fft.fftfreq(N, T)[:N//2]

    return xf[scipy.signal.find_peaks(yf, height=7*np.std(yf))[0]]  # TODO: determine better height threshold

def frequency_to_note(freq):
    """Convert a frequency `freq` from Hz to a musical note.
    
    Parameters
    ----------
    freq : float
        The frequency in Hz.
    
    Returns
    -------
    str
        The musical note.
    
    See Also
    --------
    MusicalNotes : Musical notes in Hz.
    """
    pass
