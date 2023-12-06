from modules.CleanUp import CleanUp
from modules.WaveManip import WaveManip
from modules.RT60 import calcRT60


def get_input():
    file = input("Path to file: ")
    if str(file.split(".",1)[1].upper()) == "MP3":
        return file
    elif str(file.split(".",1)[1].upper()) == "WAV":
        return file
    else:
        print("File format not supported.")
        quit()


def main():
    stream = str(get_input())
    stream = CleanUp(stream).convert()
    WaveManip(stream).wavePlot()
    calcRT60(stream)


if __name__ == '__main__':
    main()
