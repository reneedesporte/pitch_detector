"""Main program functionality, including interactions with users."""

from pitch_detector.utils import record, extract_pitch, frequency_to_note

if __name__ == "__main__":

    SAMPLE_RATE = 44100
    DURATION = 3
    data = record(DURATION, SAMPLE_RATE)

    pitches = extract_pitch(data)
    print(f"There were {len(pitches)} peak pitches found.")
    if len(pitches) == 0:
        exit()

    notes = []
    octaves = []
    for pitch in pitches:
        note, octave = frequency_to_note(pitch)
        notes.append(note)
        octaves.append(octave)

    print(
        f"The most prominent frequency was {pitches[0]} Hz, "
        f"which is a {notes[0]} note in octave {octaves[0]}."
    )
