from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt


class GraphControlPanel(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        # self.backgroundColor = "red"
        self.config(
            labelwidget=ttk.Label(
                text="GraphControlPanel",
                font=controller.labelFrameFont,
                foreground="grey",
                background=self.backgroundColor,
            ),
            background=self.backgroundColor,
        )
        self.controller = controller
        self.dropDownGraph = ttk.Combobox(
            self,
            value=["graph1", "graph2", "graph3", "graph4"],
            font=controller.dropDownFont,
            state="readonly",
            width=7,
        )

        self.dropDownGraph.current(0)
        self.dropDownGraph.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set()
        )

        self.dropDownX = ttk.Combobox(
            self,
            value=controller.dataName,
            font=controller.dropDownFont,
            state="readonly",
            width=10,
        )
        self.xLabel = Label(
            self,
            text="X",
            font=controller.labelFont,
            background=self.backgroundColor,
            foreground="black",
            border=2,
            relief="groove",
            padx=10,
            pady=5,
        )

        self.dropDownX.current(0)
        self.dropDownX.bind("<FocusIn>", lambda event: event.widget.master.focus_set())

        self.dropDownY = ttk.Combobox(
            self,
            value=controller.dataName,
            font=controller.dropDownFont,
            state="readonly",
            width=10,
        )

        self.yLabel = Label(
            self,
            text="Y",
            font=controller.labelFont,
            background=self.backgroundColor,
            foreground="black",
            border=2,
            relief="groove",
            padx=10,
            pady=5,
        )

        self.dropDownY.current(0)
        self.dropDownY.bind("<FocusIn>", lambda event: event.widget.master.focus_set())

        self.btnStyle = ttk.Style()
        self.btnStyle.configure("my.TButton", font=controller.buttonFont)

        self.plotBtn = ttk.Button(
            self, text="plot", command=self.plotIt, style="my.TButton"
        )

        self.customPlotBtn = ttk.Button(
            self, text="externPlot", command=self.externPlotIt, style="my.TButton"
        )

        self.realTimePlotBtn = ttk.Button(
            self,
            text="RealTime",
            command=self.initRealTimeParameter,
            style="my.TButton",
        )

        self.realTimeRangeOptions = ["all data", "5s", "10s"]
        self.dropDownRealTimeRangeOptions = ttk.Combobox(
            self,
            value=self.realTimeRangeOptions,
            font=controller.dropDownFont,
            state="readonly",
            width=15,
        )
        self.dropDownRealTimeRangeOptions.current(0)
        self.dropDownRealTimeRangeOptions.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set()
        )

        self.xLabel.pack(side=LEFT, padx=5)
        self.dropDownX.pack(side=LEFT, padx=5)
        self.yLabel.pack(side=LEFT, padx=5)
        self.dropDownY.pack(side=LEFT, padx=5)

        self.pack(1)

    def updateDropDownXY(self):
        print("update", self.controller.dataName)
        self.dropDownX.config(values=self.controller.dataName)
        self.dropDownY.config(values=self.controller.dataName)
        self.dropDownX.current(0)
        self.dropDownY.current(0)

    def plotIt(self):
        graphNum = self.dropDownGraph.get()
        xValue = self.controller.data[self.dropDownX.current()]
        yValue = self.controller.data[self.dropDownY.current()]
        xTitle = self.dropDownX.get()
        yTitle = self.dropDownY.get()

        self.controller.graphFrame.plot(graphNum, xValue, yValue, xTitle, yTitle)

    def externPlotIt(self):
        plt.plot(
            self.controller.data[self.dropDownX.current()],
            self.controller.data[self.dropDownY.current()],
            color="#444444",
            linestyle="--",
            label="label",
        )
        plt.title("cutomGraph")
        plt.xlabel(self.dropDownX.get())
        plt.ylabel(self.dropDownY.get())
        plt.show()

    def initRealTimeParameter(self):
        if self.dropDownX.get() == "" or self.dropDownY.get() == "":
            print("please select data to be plot")
        else:
            self.controller.graphFrame.realTimeXIndex = self.dropDownX.current()
            self.controller.graphFrame.realTimeYIndex = self.dropDownY.current()
            self.controller.graphFrame.realTimeXTitle = self.dropDownX.get()
            self.controller.graphFrame.realTimeYTitle = self.dropDownY.get()
            self.controller.graphFrame.realTimeRange = (
                self.dropDownRealTimeRangeOptions.get()
            )
            self.controller.graphFrame.realTime = True
            self.controller.graphFrame.startRealTimePlotThread()

    def pack(self, inRealTime):
        if inRealTime:
            self.dropDownGraph.pack_forget()
            self.plotBtn.pack_forget()
            self.customPlotBtn.pack_forget()
            self.dropDownRealTimeRangeOptions.pack(side=LEFT, padx=5)
            self.realTimePlotBtn.pack(side=LEFT, padx=5)

        else:
            self.dropDownRealTimeRangeOptions.pack_forget()
            self.realTimePlotBtn.pack_forget()
            self.dropDownGraph.pack(side=LEFT, padx=5)
            self.plotBtn.pack(side=LEFT, padx=5)
            self.customPlotBtn.pack(side=LEFT, padx=5)

        self.update()
