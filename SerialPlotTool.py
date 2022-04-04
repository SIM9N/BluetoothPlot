from math import fabs
from tkinter import *

from numpy import empty
from Container import *
from left.SerialPanel import SerialPanel
from left.SerialDataFrame import SerialDataFrame
from left.LoggingPanel import LoggingPanel
from right.GraphControlPanel import GraphControlPanel
from right.GraphFrame import GraphFrame
import serial
import serial.tools.list_ports
import threading as threading
import queue as queue


def readSerialDataThread(serialPort, thread_queue=None):
    result = ""
    while serialPort.isOpen():
        if serialPort.in_waiting:
            try:
                recentPacket = serialPort.readline()
            except:
                break
            result = recentPacket.decode("utf")
            thread_queue.put(result)
    print("reading thread terminated")


class SerialPlotTool(Tk):
    labelFrameFont = ("Courier New", "14", "bold")
    labelFont = ("Courier New", "13")
    dropDownFont = ("Courier New", "13")
    buttonFont = ("Courier New", "14")
    textFont = ("Courier New", "11")

    serialPort = serial.Serial()
    packetString = ""
    dataNameInited = False
    started = False
    dataName = [""]
    data = []
    appendingData = False

    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.call("source", "./Azure-ttk-theme-main/azure.tcl")
        self.call("set_theme", "light")
        self.geometry(geometry)
        self.config(bg="grey")
        self.resizable(0, 0)

        self.left = LeftContainer(self)
        self.left.place(relwidth=0.25, relheight=1, x=0, y=0)

        self.right = RightContainer(self)
        self.right.place(relwidth=0.75, relheight=1, x=300, y=0)

        self.serialPanel = SerialPanel(self.left, self)
        self.serialPanel.grid(column=0, row=0, padx=4,
                              pady=(3, 0), sticky="NESW")

        self.loggingPanel = LoggingPanel(self.left, self)
        self.loggingPanel.grid(column=0, row=1, padx=4,
                               pady=(3, 0), sticky="NESW")

        self.serialDataFrame = SerialDataFrame(self.left, self)
        self.serialDataFrame.grid(column=0, row=2, padx=4,
                                  pady=(3, 3), sticky="NESW")

        self.graphControlPanel = GraphControlPanel(self.right, self)
        self.graphControlPanel.place(relwidth=0.99, relheight=0.1, x=4, y=0)

        self.graphFrame = GraphFrame(self.right, self)
        self.graphFrame.place(relwidth=0.99, relheight=0.89, x=4, y=72)

    def defocus(event):
        event.widget.master.focus_set()

    def startReadingThread(self):
        self.threadQueue = queue.Queue()
        self.readingThread = threading.Thread(
            target=readSerialDataThread, args=(self.serialPort, self.threadQueue))
        self.readingThread.start()
        print("started reading serial thread")
        self.after(10, self.listenForData)

    def listenForData(self):
        try:
            self.packetString = self.threadQueue.get(0)
            self.serialDataFrame.insert2Text(self.packetString)
            self.checkCMD()
            self.appendData()
            self.after(1, self.listenForData)
        except queue.Empty:
            if self.readingThread.is_alive:
                self.after(100, self.listenForData)

    def checkCMD(self):
        if not self.dataNameInited:
            if self.packetString.find("dataName") == 0:
                print("found dataName")
                # self.serialPanel.startBtn.config(state="enable")
                self.dataName = self.packetString.strip("\n").split("-")
                self.dataName.pop(0)
                self.data = [[None] for i in range(len(self.dataName))]
                self.graphControlPanel.updateDropDownXY()
                self.dataNameInited = True
                self.started = True
        if self.packetString.find("save") == 0:
            print("found save")
            self.loggingPanel.autoExport("save")
        elif self.packetString.find("end") == 0:
            print("found end")
            self.loggingPanel.autoExport("end")

    def getPacketArray(self):
        return self.packetString.strip("\n").split(",")

    def appendData(self):
        if self.started and self.dataNameInited:
            packetArray = self.getPacketArray()
            if(len(packetArray) == len(self.data)):
                floatArray = []
                try:
                    for string in packetArray:
                        floatArray.append(float(string))

                    self.appendingData = True
                    for i in range(len(self.data)):
                        self.data[i].append(floatArray[i])
                    self.appendingData = False
                except:
                    print("failed append data")
                    return


app = SerialPlotTool("SerialPlotTool", "1200x700")
app.mainloop()
