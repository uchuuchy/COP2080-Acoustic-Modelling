import ffmpeg
import wave


class CleanUp:
    def __init__(self, stream: str):
        self._stream = stream

    def convert(self):
        if str(self._stream.split(".", 1)[1].upper()) == "MP3":
            (
                ffmpeg
                .input(self._stream)
                .output(self._stream.replace(".mp3", ".wav"), ac=1)
                .run(overwrite_output=True, quiet=True)
            )
            return self._stream.replace(".mp3", ".wav")
        elif str(self._stream.split(".", 1)[1].upper()) == "WAV":
            wr = wave.open(self._stream, 'r')
            if wr.getnchannels() >= 2:
                (
                    ffmpeg
                    .input(self._stream)
                    .output(f'{self._stream}-Mono', ac=1)
                    .run(overwrite_output=True, quiet=True)
                )
                wr.close()
                return f'{self._stream}-Mono'
            else:
                return self._stream
