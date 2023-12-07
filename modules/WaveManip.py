import matplotlib.pyplot as plt
import numpy as np
import wave

class WaveManip:
    def __init__(self, _stream: str):
        self.__stream = _stream
        self.__spf = wave.open(self.__stream, "r")
        self.__signal = self.__spf.readframes(-1)
        self.__signal = np.fromstring(self.__signal, "int16")
        self.__fs = self.__spf.getframerate()
        self.__time = np.linspace(0, len(self.__signal) / self.__fs, num=len(self.__signal))

    def wave_plot(self):
        plt.figure().set_size_inches(4.3125, 3.219)
        plt.title(f"Wave Form")
        plt.plot(self.__time, self.__signal)
        plt.savefig(f"./assets/wave_form.png")
        return f"./assets/wave_form.png"

