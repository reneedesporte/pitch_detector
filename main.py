"""Main program functionality, including interactions with users."""

from pitch_detector.utils import record, extract_pitch

if __name__ == "__main__":

    SECONDS = 5
    data = record(SECONDS)
    pitches = extract_pitch(data)
    print(f"There were {len(pitches)} peak pitches found: {pitches}.")
