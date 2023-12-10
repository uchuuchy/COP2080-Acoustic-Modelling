import matplotlib.pyplot as plt
import numpy as np
import wave


# Modified code from
# https://stackoverflow.com/questions/18625085/how-to-plot-a-wav-file
# to be modular and better interact with the gui
class WaveManip:
    def __init__(self, _stream: str):
        self.__stream = _stream
        self.__spf = wave.open(self.__stream, "r")
        self.__signal = self.__spf.readframes(-1)
        self.__signal = np.fromstring(self.__signal, "int16")
        self.__fs = self.__spf.getframerate()
        self.__time = np.linspace(0, len(self.__signal) / self.__fs, num=len(self.__signal))

    # Plots the wave form
    def wave_plot(self):
        plt.figure().set_size_inches(4.80, 3.36)
        plt.title(f"Wave Form")
        plt.xlabel('Time (s)')
        plt.ylabel("Signal (Hz)")
        plt.plot(self.__time, self.__signal)
        plt.plot(self.__time[np.argmax(self.__signal)], self.__signal.max(), "yo")
        plt.savefig(f"./assets/graphs/wave_form.png", bbox_inches="tight")
        plt.close()
        return f"./assets/graphs/wave_form.png"

    def get_time(self):
        return round(self.__time.max(), 2)

    def get_highest_freq(self):
        return self.__signal.max()

