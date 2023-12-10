import tkinter


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, Label

# Acoustic Modelling Modules
from modules.CleanUp import CleanUp
from modules.WaveManip import WaveManip
from modules.AcousticModel import AcousticModel

###


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")


# Handles how the user interaction with the GUI interfaces with the logic which models the audio file.
class Controller:
    # Initializes variables such as:
    # filename: str
    # stores the path to the file chosen in the file dialog box when the load button is pressed.
    # graphs: array
    # stores paths to the images of the generated graphs
    # current_index : int
    # keeps track of which graph to display
    # max: int
    # stores the max index value of the graphs array
    def __init__(self):
        self.__filename = ""
        self.__graphs = []
        self.__current_index = 0
        self.__max = 0

    # Calculates the max index value of the graphs array
    def __calc_max(self):
        self.__max = len(self.__graphs) - 1

    # Handles advancing the array of images and displays it. If the user is at the final index, it will reset
    # the index to 0 and bring them back to the start.
    def next_graph(self):
        if self.__current_index < self.__max:
            self.__current_index += 1
            canvas.itemconfig(image_2, image_image_2.configure(file=self.__graphs[self.__current_index]))
        else:
            self.__current_index = 0
            canvas.itemconfig(image_2, image_image_2.configure(file=self.__graphs[self.__current_index]))

    # Handles regressing the array of images and displays it. If the user is at the first index, it will set
    # the index to the max value and bring them to the end.
    def previous_graph(self):
        if self.__current_index > 0:
            self.__current_index -= 1
            canvas.itemconfig(image_2, image_image_2.configure(file=self.__graphs[self.__current_index]))
        else:
            self.__current_index = self.__max
            canvas.itemconfig(image_2, image_image_2.configure(file=self.__graphs[self.__current_index]))

    # Handles updating the labels on the GUI and running the acoustic modelling code
    def __run_model(self):
        # self.__filename = CleanUp(self.__filename).convert()
        # could not get conversions to work

        self.__update_label(entry_2, f"Time (Seconds):\n{WaveManip(self.__filename).get_time()}")

        acoustic_model = AcousticModel(self.__filename)

        self.__graphs.append(WaveManip(self.__filename).wave_plot())
        self.__graphs.append(acoustic_model.get_decibel_over_time())
        self.__graphs.append(acoustic_model.get_spectrogram())
        self.__graphs.append(acoustic_model.get_low_rt60_graph())
        self.__graphs.append(acoustic_model.get_mid_rt60_graph())
        self.__graphs.append(acoustic_model.get_high_rt60_graph())
        self.__calc_max()

        self.__update_label(entry_3, f"RT60 Value (Seconds):\n{acoustic_model.get_rt60_value()}")
        self.__update_label(entry_4, f"Highest Frequency (Hz):\n{WaveManip(self.__filename).get_highest_freq()}")
        canvas.itemconfig(image_2, image_image_2.configure(file=self.__graphs[0]))

    # Updates labels on the GUI
    @staticmethod
    def __update_label(label: Label, stream: str):
        label.configure(text=stream)

    # Resets initial variables and allows user to select a file.
    # After a file is selected, it will try to run the model,
    # if this fails, like if a file is not selected, it will give a dialog box with the error.
    def browse_files(self):
        try:
            self.__filename = ""
            self.__graphs = []
            self.__current_index = 0
            self.__max = 0
            self.__filename = filedialog.askopenfilename(initialdir=".",
                                                  title="Select a File",
                                                  filetypes=(("WAVE file",
                                                              "*.wav*"),
                                                             ("MP3 file",
                                                              "*.mp3*")))
            # Change label contents
            entry_1.configure(text="File Opened: " + self.__filename)
            try:
                self.__run_model()
            except:
                messagebox.showerror('Python Error', 'No file selected')
        except Exception as error:
            messagebox.showerror('Python Error', error)


# Initializes a Controller object
gui_controller = Controller()


######################################################
# The code below was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer
# I've made minor edits to it such as changing the button functions
# and changing Text() objects to Label() objects

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("750x500")
window.configure(bg = "#FFFFFF")
window.title("COP2080 Acoustic Modelling Project")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 500,
    width = 750,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    375.0,
    250.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    329.0,
    33.0,
    image=entry_image_1
)
entry_1 = Label(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=14.0,
    y=19.0,
    width=630.0,
    height=26.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=gui_controller.browse_files,
    relief="flat"
)
button_1.place(
    x=657.0,
    y=19.0,
    width=78.0,
    height=28.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    254.0,
    246.0,
    image=image_image_2
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=gui_controller.previous_graph,
    relief="flat"
)
button_2.place(
    x=14.0,
    y=433.0,
    width=78.0,
    height=28.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=gui_controller.next_graph,
    relief="flat"
)
button_3.place(
    x=116.0,
    y=433.0,
    width=78.0,
    height=28.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    621.0,
    134.0,
    image=entry_image_2
)
entry_2 = Label(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=507.0,
    y=78.0,
    width=228.0,
    height=110.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    621.0,
    246.0,
    image=entry_image_3
)
entry_3 = Label(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=507.0,
    y=190.0,
    width=228.0,
    height=110.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    621.0,
    358.0,
    image=entry_image_4
)
entry_4 = Label(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=507.0,
    y=302.0,
    width=228.0,
    height=110.0
)
window.resizable(False, False)
window.mainloop()
