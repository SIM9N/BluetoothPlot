from tkinter import *

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
        try:
            if serialPort.in_waiting:
                recentPacket = serialPort.readline()
                result = recentPacket.decode("utf")
                thread_queue.put(result)
                # print(thread_queue.qsize())
                if thread_queue.qsize() > 6:
                    while thread_queue.qsize() > 3:
                        string = thread_queue.get(False)
                        if (
                            string.find("dataName") != -1
                            or string.find("save") != -1
                            or string.find("end") != -1
                        ):
                            thread_queue.put(string)
                            print("put again")

        except Exception as e:
            continue
    print("readingThread terminated")


class SerialPlotTool(Tk):
    labelFrameFont = ("Courier New", "14", "bold")
    labelFont = ("Courier New", "13")
    dropDownFont = ("Courier New", "13")
    buttonFont = ("Courier New", "14")
    textFont = ("Courier New", "11")

    serialPort = serial.Serial()
    packetString = ""
    dataNameInited = False
    dataName = [""]
    data = []
    dataLock = threading.Lock()

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
        self.serialPanel.grid(column=0, row=0, padx=4, pady=(3, 0), sticky="NESW")

        self.loggingPanel = LoggingPanel(self.left, self)
        self.loggingPanel.grid(column=0, row=1, padx=4, pady=(3, 0), sticky="NESW")

        self.serialDataFrame = SerialDataFrame(self.left, self)
        self.serialDataFrame.grid(column=0, row=2, padx=4, pady=(3, 3), sticky="NESW")

        self.graphControlPanel = GraphControlPanel(self.right, self)
        self.graphControlPanel.place(relwidth=0.99, relheight=0.1, x=4, y=0)

        self.graphFrame = GraphFrame(self.right, self)
        self.graphFrame.place(relwidth=0.99, relheight=0.89, x=4, y=72)

    def defocus(event):
        event.widget.master.focus_set()

    def startReadingThread(self):
        self.threadQueue = queue.Queue()
        self.readingThread = threading.Thread(
            target=readSerialDataThread, args=(self.serialPort, self.threadQueue)
        )
        self.readingThread.start()
        print("readingThread started")
        self.after(1, self.listenForData)

    def listenForData(self):
        if not self.serialPort.isOpen():
            return
        try:
            self.packetString = self.threadQueue.get(False)
            self.serialDataFrame.insert2Text(self.packetString)
            # print(int(self.serialDataFrame.textData.index("end").split(".")[0]) - 1)
            if int(self.serialDataFrame.textData.index("end").split(".")[0]) - 1 > 500:
                self.serialDataFrame.textData.delete(1.0, 200.0)
            self.checkCMD()
            self.appendData()
            self.after(1, self.listenForData)
            # print("packetString" + self.packetString)
        except queue.Empty:
            # print("exception on listenForData")
            if self.readingThread.is_alive:
                self.after(1, self.listenForData)

    def checkCMD(self):
        if self.packetString.find("dataName") == 0:
            print("dataName initialized, data reset")
            # self.serialPanel.startBtn.config(state="enable")
            self.dataName = self.packetString.strip("\n").split("-")
            self.dataName.pop(0)
            self.data = [[None] for i in range(len(self.dataName))]
            self.graphControlPanel.updateDropDownXY()
            self.dataNameInited = True
        if self.dataNameInited:
            if self.packetString.find("save") == 0:
                print("start exporting")
                self.loggingPanel.exportStartIndex = len(self.data[0]) - 1
            elif self.packetString.find("end") == 0:
                print("end exporting")
                self.loggingPanel.exportEndIndex = len(self.data[0]) - 1
                self.loggingPanel.autoExport()

    def getPacketArray(self):
        return self.packetString.strip("\n").split(",")

    def appendData(self):
        if self.dataNameInited:
            packetArray = self.getPacketArray()
            if len(packetArray) == len(self.data):
                floatArray = []
                for string in packetArray:
                    floatArray.append(float(string))
                try:
                    if self.dataLock.acquire(False):
                        for i in range(len(self.data)):
                            self.data[i].append(floatArray[i])
                finally:
                    self.dataLock.release()


app = SerialPlotTool("SerialPlotTool", "1200x700")
app.mainloop()
