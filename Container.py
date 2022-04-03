import imp
from tkinter import *
from LoggingPanel import LoggingPanel
from SerialPanel import SerialPanel
from SerialDataFrame import SerialDataFrame
from GraphControlPanel import GraphControlPanel
from GraphFrame import GraphFrame


class LeftContainer(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.backgroundColor = "#E0FFFF"
        self.config(bg=self.backgroundColor, bd=3, relief="groove")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=6)

        self.serialPanel = SerialPanel(self)
        self.serialPanel.grid(column=0, row=0, padx=4,
                              pady=(3, 0), sticky="NESW")

        self.loggingPanel = LoggingPanel(self)
        self.loggingPanel.grid(column=0, row=1, padx=4,
                               pady=(3, 0), sticky="NESW")

        self.serialDataFrame = SerialDataFrame(self)
        self.serialDataFrame.grid(column=0, row=2, padx=4,
                                  pady=(3, 3), sticky="NESW")


class RightContainer(Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.backgroundColor = "#78AFD4"
        self.backgroundColor = "white"
        self.config(bg=self.backgroundColor, bd=3, relief="groove")

        self.graphControlPanel = GraphControlPanel(self)
        self.graphControlPanel.place(relwidth=0.99, relheight=0.1, x=4, y=0)

        self.graphFrame = GraphFrame(self)
        self.graphFrame.place(relwidth=0.99, relheight=0.89, x=4, y=72)
