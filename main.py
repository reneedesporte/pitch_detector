"""Main program functionality, including interactions with users."""

import time
import sounddevice as sd
from pitch_detector.log import Logger
from pitch_detector.buffer import Buffer

log = Logger()
buffer = Buffer(log)  # TODO does this need to be global?

def callback(indata, frames, time, status):
    """
    Main callback function for audio data.

    See Also
    --------
    sounddevice.InputStream
    """
    if any(indata):
        data = indata
        buffer.put(data)

if __name__ == "__main__":

    SAMPLE_RATE = 44100
    DURATION = 3
    input_device_index, _ = sd.default.device
    devices = sd.query_devices()

    log.write(f"Recording on '{devices[input_device_index]['name']}'!")
    stream = sd.InputStream(
        device=input_device_index, channels=1,
        samplerate=SAMPLE_RATE, callback=callback
    )

    stream.start()

    try:
        buffer.process()
    except KeyboardInterrupt:
        log.write("Quitting at user request.")
    except Exception as e:
        log.write(f"Exiting due to exception: {e}!")

    stream.stop()
    log.shutdown()
