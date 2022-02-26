from cgitb import text
from sqlite3 import connect
from textwrap import fill
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import color, width
import serial.tools.list_ports
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure


root = Tk()
root.title("BluetoothPlot")
root.config(bg="grey")
root.geometry("1000x600")
root.minsize(1000, 600)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

leftWrapperFrame = Frame(root, bg="#8ab2b4", bd=2, relief=RIDGE)
leftWrapperFrame.grid(column=0, row=0, sticky="nesw")

rightWrapperFrame = Frame(root, bg="#c9eeeb", bd=2, relief=RIDGE)
rightWrapperFrame.grid(column=1, row=0, sticky="nesw")

# --- Start Left Part ---#
leftWrapperFrame.grid_columnconfigure(0, weight=1)
leftWrapperFrame.grid_rowconfigure(0, weight=1)
leftWrapperFrame.grid_rowconfigure(1, weight=3)

# serial port
serialFrame = Frame(leftWrapperFrame, bg="#a4b2b0")
serialFrame.grid(column=0, row=0, padx=5, pady=5, sticky="nesw")


def defocus(event):
    event.widget.master.focus_set()


# selecting the serial port
serialPortOptions = ["0"]
avaPorts = serial.tools.list_ports.comports()
serialObj = serial.Serial()

for onePort in avaPorts:
    serialPortOptions.append(str(onePort).split(" ")[0])

portLabel = Label(serialFrame, text="Port:", font=("Courier New", "9"))

dropDownSerialOptions = ttk.Combobox(
    serialFrame,
    value=serialPortOptions,
    font=("Courier New", "10"),
    state="readonly",
)

dropDownSerialOptions.current(0)
dropDownSerialOptions.bind("<FocusIn>", defocus)

# selecting the serial baudrate
baudrateOptions = [1800, 2400, 4800, 9600, 19200, 28800, 38400, 57600, 76800, 115200]

baudrateLabel = Label(serialFrame, text="Baudrate:", font=("Courier New", "9"))

dropDownBaudrateOptions = ttk.Combobox(
    serialFrame,
    value=baudrateOptions,
    font=("Courier New", "10"),
    state="readonly",
)
dropDownBaudrateOptions.current(len(baudrateOptions) - 1)
dropDownBaudrateOptions.bind("<FocusIn>", defocus)

# connect the selected comport
def initComPort():
    try:
        serialObj.port = dropDownSerialOptions.get()
        serialObj.baudrate = dropDownBaudrateOptions.get()
        serialObj.close()
        serialObj.open()
    except IOError as e:
        messagebox.showerror(
            "Error",
            "Error, can't connect to "
            + dropDownSerialOptions.get()
            + "\n\n"
            + "( "
            + str(e)
            + " )",
        )


# some btnssssssss
connectBtn = Button(serialFrame, text="connect", command=initComPort)

disconnectBtn = Button(
    serialFrame, text="disconnect", command=lambda: serialObj.close()
)


# Bluetooth data print
dataFrame = Frame(leftWrapperFrame, bg="#bbc1c8")
dataFrame.grid(column=0, row=1, padx=5, pady=5, sticky="nesw")

textData = Text(dataFrame, wrap=NONE, font=("Courier New", "8"), takefocus=0)

dataCanvasScrollbar = ttk.Scrollbar(dataFrame, orient=VERTICAL, command=textData.yview)
dataCanvasScrollbar2 = ttk.Scrollbar(
    dataFrame, orient=HORIZONTAL, command=textData.xview
)

textData["yscroll"] = dataCanvasScrollbar.set
textData["xscroll"] = dataCanvasScrollbar2.set


def printSerialPortData():
    if serialObj.isOpen() and serialObj.in_waiting:
        recentPacket = serialObj.readline()
        recentPacketString = recentPacket.decode("utf")
        textData.insert("end", recentPacketString)


# clean the text in dataFrame
def cleanData():
    textData.delete(1.0, END)


cleanBtn = Button(serialFrame, text="clean", command=cleanData)

# --- End Left Part ---#

# --- Start Right Part ---#
fig = Figure(figsize=(0.5, 0.5), dpi=100)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)

ax1.plot(
    [0, 1, 2, 3, 4, 5, 6, 7, 9],
    [1, 5, 3, 7, 9, 2, 9, 2, 0],
    color="#444444",
    linestyle="--",
    label="label",
)
ax1.legend()
ax1.set_title("graph1")
ax1.set_xlabel("xlabel")
ax1.set_ylabel("ylabel")

ax2.plot([0, 1, 2, 3, 4, 5, 6, 7, 9], [1, 5, 3, 7, 9, 2, 9, 2, 0])
ax2.legend()
ax2.set_title("graph2")
ax2.set_xlabel("xlabel")
ax2.set_ylabel("ylabel")


class Toolbar(NavigationToolbar2Tk):
    def set_message(self, s):
        pass


graphCanvas = FigureCanvasTkAgg(fig, rightWrapperFrame)
graphCanvas.draw()
graphToolBar = Toolbar(graphCanvas, rightWrapperFrame, pack_toolbar=False)
graphToolBar.update()


# --- End Right Part ---#


# update the place when root resize
def place():

    portLabel.place(relheight=0.15, relwidth=1 - 0.8, x=2, y=0)

    dropDownSerialOptions.place(
        anchor=NE, relwidth=0.75, relheight=0.15, x=serialFrame.winfo_width() - 2, y=0
    )

    baudrateLabel.place(
        relheight=0.15, relwidth=1 - 0.7, x=2, y=10 + portLabel.winfo_height()
    )

    dropDownBaudrateOptions.place(
        anchor=NE,
        relwidth=0.65,
        relheight=0.15,
        x=serialFrame.winfo_width() - 2,
        y=10 + dropDownSerialOptions.winfo_height(),
    )

    connectBtn.place(
        relwidth=0.47,
        relheight=0.15,
        x=2,
        y=20 + baudrateLabel.winfo_height() + portLabel.winfo_height(),
    )

    disconnectBtn.place(
        anchor=NE,
        relwidth=0.47,
        relheight=0.15,
        x=serialFrame.winfo_width() - 2,
        y=20
        + dropDownSerialOptions.winfo_height()
        + dropDownBaudrateOptions.winfo_height(),
    )

    cleanBtn.place(
        relwidth=0.47,
        relheight=0.15,
        x=2,
        y=30
        + baudrateLabel.winfo_height()
        + portLabel.winfo_height()
        + connectBtn.winfo_height(),
    )

    textData.place(
        anchor=NW,
        x=0,
        y=0,
        relheight=0.95,
        relwidth=0.95,
    )

    dataCanvasScrollbar.place(
        anchor=NE,
        x=serialFrame.winfo_width() - 2,
        y=0,
        relwidth=0.08,
        relheight=1,
    )

    dataCanvasScrollbar2.place(
        x=0,
        y=textData.winfo_height(),
        relheight=0.05,
        relwidth=0.92,
    )

    graphToolBar.place(
        anchor=SW,
        x=0,
        y=rightWrapperFrame.winfo_height() - 5,
        relwidth=1,
    )

    graphCanvas.get_tk_widget().place(
        x=0,
        y=0,
        height=rightWrapperFrame.winfo_height() - graphToolBar.winfo_height(),
        relwidth=1,
    )


def d(event):
    place()


root.bind("<Configure>", d)

while True:
    root.update_idletasks()
    root.update()
    place()
    printSerialPortData()
