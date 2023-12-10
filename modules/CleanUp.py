import pydub
import wave
from pathlib import Path

# This code never worked.
class CleanUp:
    def __init__(self, stream: str):
        self._stream = str(Path(stream))

    def convert(self):
        if str(self._stream.split(".", 1)[1].upper()) == "MP3":
            stream = pydub.AudioSegment.from_mp3(self._stream)
            stream = stream.set_channels(1)
            stream.export(str(Path(f'../sound-files/new.wav')), format="wav")
            return str(Path(f'../sound-files/new.wav'))
        elif str(self._stream.split(".", 1)[1].upper()) == "WAV":
            wr = wave.open(self._stream, 'r')
            if wr.getnchannels() >= 2:
                wr.close()
                stream = pydub.AudioSegment.from_wav(self._stream)
                stream = stream.set_channels(1)
                stream.export(f'{self._stream}-new', format="wav")
                return str(Path(f'{self._stream}-new'))
            else:
                return self._stream
