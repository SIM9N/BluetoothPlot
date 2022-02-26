from curses import window
from tkinter import *
import serial.tools.list_ports
import functools

avaPorts = serial.tools.list_ports.comports()
serialObj = serial.Serial()

root = Tk()
root.title("BluetoothPlot")
root.config(bg="grey")


def initComPort(index):
    currentPort = str(avaPorts[index])
    # print(currentPort)
    comPortVar = str(currentPort.split(" ")[0])
    # print(comPortVar)
    serialObj.port = comPortVar
    serialObj.baudrate = 115200
    serialObj.open()


for onePort in avaPorts:
    comButton = Button(
        root,
        text=onePort,
        font=("Calibri", "13"),
        height=1,
        width=45,
        command=functools.partial(initComPort, index=avaPorts.index(onePort)),
    )
    comButton.grid(row=avaPorts.index(onePort), column=0)

dataCanvas = Canvas(root, width=600, height=400, bg="grey")
dataCanvas.grid(row=0, column=1, rowspan=100)

scrollBar = Scrollbar(root, orient="vertical", command=dataCanvas.yview)
scrollBar.grid(row=0, column=2, rowspan=100, sticky="ns")

dataCanvas.config(yscrollcommand=scrollBar.set)

dataFrame = Frame(dataCanvas, bg="white")
dataCanvas.create_window((10, 0), window=dataFrame, anchor="nw")


def checkSerialPort():
    if serialObj.isOpen() and serialObj.in_waiting:
        recentPacket = serialObj.readline()
        recentPacketString = recentPacket.decode("utf").rstrip("\n")
        Label(
            dataFrame, text=recentPacketString, font=("Calibri", "13"), bg="white"
        ).pack()


while True:
    root.update()
    checkSerialPort()
    dataCanvas.config(scrollregion=dataCanvas.bbox("all"))
