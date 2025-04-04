"""Module containing the data collection and processing functionality."""

import math
import scipy
import numpy as np
import sounddevice as sd

MUSICAL_NOTES = {}
MUSICAL_NOTES["C"] = 16.35
MUSICAL_NOTES["C#"] = 17.32
MUSICAL_NOTES["D"] = 18.35
MUSICAL_NOTES["D#"] = 19.45
MUSICAL_NOTES["E"] = 20.60
MUSICAL_NOTES["F"] = 21.83
MUSICAL_NOTES["F#"] = 23.12
MUSICAL_NOTES["G"] = 24.50
MUSICAL_NOTES["G#"] = 25.96
MUSICAL_NOTES["A"] = 27.50
MUSICAL_NOTES["A#"] = 29.14
MUSICAL_NOTES["B"] = 30.87


def record(duration, sr=44100, device=None):
    """Record `duration` seconds of audio data from the default microphone.
    
    Parameters
    ----------
    duration : int
        Seconds of data to record.
    sr : int, default=44100
        Sample rate per second.
    device : int, default=None
        Device index.
    
    Returns
    -------
    ndarray
        1-d ndarray of length `duration`*`sr`.
    """
    if device is not None:
        sd.default.device = device  # TODO: add error handling for non-existant device request
    input_device_index, _ = sd.default.device
    devices = sd.query_devices()
    print(f"Recording for {duration} seconds on '{devices[input_device_index]['name']}'!")

    data = sd.rec(duration*sr, samplerate=sr, channels=1)
    sd.wait()

    print("Done!")
    return data.flatten()

def extract_pitch(data, sr=44100, threshold=50):
    """
    Extract peaks frequencies from `data`.
    
    Parameters
    -----------
    data : ndarray
        The single-channel audio data.
    sr : int, default=44100
        Sample rate of `data`.
    threshold : int, default=50
        Multiplier of average periodogram value, which acts as threshold
         for the `find_peaks` operation.
    
    Returns
    --------
    array
        The peak frequencies of `data`, ordered by decreasing strength.
    
    See Also
    --------
    scipy.signal.periodogram
    scipy.signal.find_peaks
    """
    f, Pxx_den = scipy.signal.periodogram(data, sr)
    peaks, etc = scipy.signal.find_peaks(
        Pxx_den,
        height=threshold*np.average(Pxx_den),
    )
    peaks = f[peaks]  # Convert indices to frequencies
    peaks = np.round(peaks, 2)
    return [float(x) for _, x in sorted(zip(etc["peak_heights"], peaks), reverse=True)]

def frequency_to_note(freq):
    """Convert a frequency `freq` from Hz to a musical note.
    
    Parameters
    ----------
    freq : float
        The frequency in Hz.
    
    Returns
    -------
    str
        The musical note that closest matched `freq`.
    """
    log_val = []
    for key, val in MUSICAL_NOTES.items():
        log_val.append(math.log2(freq/val))
    octave = round(sum(log_val)/len(log_val))
    log_val = list(
        np.abs(
            np.asarray(log_val) - round(sum(log_val)/len(log_val))
        )
    )
    note = list(MUSICAL_NOTES.keys())[log_val.index(min(log_val))]
    return note, octave
