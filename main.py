"""Main program functionality, including interactions with users."""

from pitch_detector.utils import record, extract_pitch
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    SAMPLE_RATE = 44100
    DURATION = 5
    data = record(DURATION, SAMPLE_RATE)

    plt.plot(np.linspace(0, DURATION, len(data)), data)
    plt.title("Timeseries")
    plt.xlabel("Time (s)")
    plt.tight_layout()
    plt.show()

    pitches = extract_pitch(data)
    print(f"There were {len(pitches)} peak pitches found: {pitches}.")
