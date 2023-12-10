import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


# Redesign and reimplementation of code provided by Professor Navarro during an in-class lecture
# The redesign and reimplementation involved turning the provided code into a class object in order
# for its behaviour to be more modular, and to make it interact with the GUI seamlessly.
class AcousticModel:
    def __init__(self, stream):
        self.__sample_rate, self.__data = wavfile.read(stream)
        self.__spectrum, self.__frequencies, self.__t, self.__im = plt.specgram(
            self.__data,
            Fs=self.__sample_rate,
            NFFT=1024,
            cmap=plt.get_cmap('autumn_r'))

        # Turned target_frequency, index_of_frequency, and data_for_frequency into arrays.
        # This was done in order to store the needed values for the low, mid, and high
        # frequencies.
        self.__target_frequency = []
        self.find_target_frequency()
        self.__index_of_frequency = []
        self.__data_for_frequency = []
        self.calc_values()

        # Calculates the data in decibels for the low frequency, mid-frequency, and high frequency.
        # Finds the position of the highest value in the decibel data.
        self.__low_data_in_db = 10 * np.log10(self.__data_for_frequency[0], where=self.__data_for_frequency[0] > 0)
        self.__low_index_of_max = np.argmax(self.__low_data_in_db)
        self.__low_value_of_max = self.__low_data_in_db[self.__low_index_of_max]

        self.__mid_data_in_db = 10 * np.log10(self.__data_for_frequency[1], where=self.__data_for_frequency[1] > 0)
        self.__mid_index_of_max = np.argmax(self.__mid_data_in_db)
        self.__mid_value_of_max = self.__mid_data_in_db[self.__mid_index_of_max]

        self.__high_data_in_db = 10 * np.log10(self.__data_for_frequency[2], where=self.__data_for_frequency[2] > 0)
        self.__high_index_of_max = np.argmax(self.__high_data_in_db)
        self.__high_value_of_max = self.__high_data_in_db[self.__high_index_of_max]

        # Stores the RT60 values of the low, mid, and high frequencies.
        self.__rt60 = []

    # Initially, this code only contains a singular for-loop to check for a target frequency of 1Khz
    # This has been updated with two additional for loops which check for a target frequency between 60Hz and 250Hz
    # and a target frequency between 5Khz and 10Khz
    def find_target_frequency(self):
        for x in self.__frequencies:
            if 60 < x < 250:
                break
        for y in self.__frequencies:
            if y > 1000:
                break
        for z in self.__frequencies:
            if 5000 < z < 10000:
                break
        self.__target_frequency = [x, y, z]

    # Finds and saves the position and data of the target frequency.
    def calc_values(self):
        for i in range(3):
            self.__index_of_frequency.append(np.where(self.__frequencies == self.__target_frequency[i])[0][0])
            self.__data_for_frequency.append(self.__spectrum[self.__index_of_frequency[i]])

    # Graphs the decibels over time, this code is from the provided code.
    # Saves graph to assets folder
    def get_decibel_over_time(self):
        plt.figure().set_size_inches(4.80, 3.36)
        plt.plot(self.__t, self.__mid_data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.title(f"Decibel Over Time")
        plt.xlabel('Time (s)')
        plt.ylabel("Power (db)")
        plt.plot(self.__t[self.__mid_index_of_max], self.__mid_data_in_db[self.__mid_index_of_max], 'go')

        plt.savefig(f"./assets/graphs/decibel_over_time.png", bbox_inches="tight")
        plt.close()
        return f"./assets/graphs/decibel_over_time.png"

    # Graphs the spectrogram, this code is from the provided code.
    # Saves graph to assets folder
    def get_spectrogram(self):
        plt.figure().set_size_inches(4.80, 3.36)
        plt.specgram(
            self.__data,
            Fs=self.__sample_rate,
            NFFT=1024,
            cmap=plt.get_cmap('autumn_r'))
        plt.colorbar(self.__im).set_label('Intensity (dB)')
        plt.title(f"Spectrogram")
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')

        plt.savefig(f"./assets/graphs/spectrogram.png", bbox_inches="tight")
        plt.close()
        return f"./assets/graphs/spectrogram.png"

    # Graphs the RT20 graph of the low, mid, and high frequencies, this code is from the provided code
    # It has been slightly modified to give a more appealing graph
    def get_low_rt60_graph(self):
        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        sliced_array = self.__low_data_in_db[self.__low_index_of_max:]
        plt.figure().set_size_inches(4.80, 3.36)
        plt.plot(self.__t[self.__low_index_of_max:], sliced_array)
        plt.title(f"RT20 Between 60 and 250Hz")
        plt.xlabel('Time (s)')
        plt.ylabel("Power (db)")
        value_of_max_less_5 = self.__low_value_of_max - 5
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(self.__low_data_in_db == value_of_max_less_5)
        plt.plot(self.__t[index_of_max_less_5], self.__low_data_in_db[index_of_max_less_5], 'yo')

        value_of_max_less_25 = self.__low_value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(self.__low_data_in_db == value_of_max_less_25)
        plt.plot(self.__t[index_of_max_less_25], self.__low_data_in_db[index_of_max_less_25], 'ro')

        rt20 = (self.__t[index_of_max_less_5] - self.__t[index_of_max_less_25])[0]
        # RT60 Value
        self.__rt60.append(rt20 * 3)
        plt.grid()

        plt.savefig(f"./assets/graphs/low_rt20_graph.png", bbox_inches="tight")
        plt.close()
        return f"./assets/graphs/low_rt20_graph.png"

    def get_mid_rt60_graph(self):
        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        sliced_array = self.__mid_data_in_db[self.__mid_index_of_max:]
        plt.figure().set_size_inches(4.80, 3.36)
        plt.plot(self.__t[self.__mid_index_of_max:], sliced_array)
        plt.title(f"RT20 Around 1000Hz")
        plt.xlabel('Time (s)')
        plt.ylabel("Power (db)")

        value_of_max_less_5 = self.__mid_value_of_max - 5
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(self.__mid_data_in_db == value_of_max_less_5)
        plt.plot(self.__t[index_of_max_less_5], self.__mid_data_in_db[index_of_max_less_5], 'yo')

        value_of_max_less_25 = self.__mid_value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(self.__mid_data_in_db == value_of_max_less_25)
        plt.plot(self.__t[index_of_max_less_25], self.__mid_data_in_db[index_of_max_less_25], 'ro')

        rt20 = (self.__t[index_of_max_less_5] - self.__t[index_of_max_less_25])[0]
        # RT60 Value
        self.__rt60.append(rt20 * 3)
        plt.grid()

        plt.savefig(f"./assets/graphs/mid_rt20_graph.png", bbox_inches="tight")
        plt.close()
        return f"./assets/graphs/mid_rt20_graph.png"

    def get_high_rt60_graph(self):
        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        sliced_array = self.__high_data_in_db[self.__high_index_of_max:]
        plt.figure().set_size_inches(4.80, 3.36)
        plt.plot(self.__t[self.__high_index_of_max:], sliced_array)
        plt.title(f"RT20 Between 5 and 10KHz")
        plt.xlabel('Time (s)')
        plt.ylabel("Power (db)")

        value_of_max_less_5 = self.__high_value_of_max - 5
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(self.__high_data_in_db == value_of_max_less_5)
        plt.plot(self.__t[index_of_max_less_5], self.__high_data_in_db[index_of_max_less_5], 'yo')

        value_of_max_less_25 = self.__high_value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(self.__high_data_in_db == value_of_max_less_25)
        plt.plot(self.__t[index_of_max_less_25], self.__high_data_in_db[index_of_max_less_25], 'ro')

        rt20 = (self.__t[index_of_max_less_5] - self.__t[index_of_max_less_25])[0]
        # RT60 Value
        self.__rt60.append(rt20 * 3)
        plt.grid()

        plt.savefig(f"./assets/graphs/high_rt20_graph.png", bbox_inches="tight")
        plt.close()
        return f"./assets/graphs/high_rt20_graph.png"

    # Returns the average value of the rt60 values calculated from each frequency
    def get_rt60_value(self):
        return round(abs(sum(self.__rt60) / 3), 2)
