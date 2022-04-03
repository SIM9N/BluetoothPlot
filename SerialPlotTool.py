from math import fabs
from tkinter import *
from Container import *
import serial
import serial.tools.list_ports


class SerialPlotTool(Tk):
    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.call("source", "./Azure-ttk-theme-main/azure.tcl")
        self.call("set_theme", "light")
        self.geometry(geometry)
        self.config(bg="grey")
        self.resizable(0, 0)

        self.serialPort = serial.Serial()
        self.packetString = ""
        self.dataNameInited = False
        self.started = False
        self.dataName = [""]
        self.data = []

        self.left = LeftContainer(self)
        self.left.place(relwidth=0.25, relheight=1, x=0, y=0)

        self.right = RightContainer(self)
        self.right.place(relwidth=0.75, relheight=1, x=300, y=0)

    def getAndPrintData(self):
        if self.serialPort.isOpen() and self.serialPort.in_waiting:
            # clear the buffer, otherwise as time goes on, the delay become larger, and new and old data will be read
            if self.serialPort.in_waiting >= 500:
                app.serialPort.flushInput()
                recentPacket = self.serialPort.readline()
                return
            recentPacket = self.serialPort.readline()
            try:
                self.packetString = recentPacket.decode("utf")
                self.left.serialDataFrame.insert2Text(self.packetString)
            except:
                print("can't decode utf")

    def initDataName(self):
        if not self.dataNameInited:
            if self.packetString.find("dataName") == 0:
                print("found dataName")
                self.left.serialPanel.startBtn.config(state="enable")
                self.dataName = self.packetString.strip("\n").split("-")
                self.dataName.pop(0)
                self.data = [[None] for i in range(len(self.dataName))]
                self.right.graphControlPanel.updateDropDownXY()
                self.dataNameInited = True

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

                    for i in range(len(self.data)):
                        self.data[i].append(floatArray[i])
                except:
                    return


app = SerialPlotTool("SerialPlotTool", "1200x700")
while(True):
    app.update_idletasks()
    app.update()
    app.right.graphFrame.realTimePlot()
    app.getAndPrintData()
    app.initDataName()
    app.appendData()
