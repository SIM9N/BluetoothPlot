from tkinter import*
from tkinter import ttk
import matplotlib.pyplot as plt


class GraphControlPanel(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        # self.backgroundColor = "red"
        self.config(labelwidget=ttk.Label(
            text="GraphControlPanel", font=controller.labelFrameFont, foreground="grey", background=self.backgroundColor), background=self.backgroundColor)
        self.controller = controller
        self.dropDownGraph = ttk.Combobox(
            self,
            value=["graph1", "graph2", "graph3", "graph4"],
            font=controller.dropDownFont,
            state="readonly",
            width=7,
        )
        self.graphLabel = Label(
            self, text="plot", font=controller.labelFont, background=self.backgroundColor, foreground="black", border=2, relief="groove", padx=10, pady=5
        )
        self.graphLabel.pack(side=LEFT, padx=5)

        self.dropDownGraph.current(0)
        self.dropDownGraph.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set())
        self.dropDownGraph.pack(side=LEFT, padx=5)

        self.dropDownX = ttk.Combobox(
            self,
            value=controller.dataName,
            font=controller.dropDownFont,
            state="readonly",
            width=10,
        )
        self.xLabel = Label(self, text="X", font=controller.labelFont, background=self.backgroundColor,
                            foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.xLabel.pack(side=LEFT, padx=5)

        self.dropDownX.current(0)
        self.dropDownX.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set())
        self.dropDownX.pack(side=LEFT, padx=5)

        self.dropDownY = ttk.Combobox(
            self,
            value=controller.dataName,
            font=controller.dropDownFont,
            state="readonly",
            width=10,
        )

        self.yLabel = Label(self, text="Y", font=controller.labelFont, background=self.backgroundColor,
                            foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.yLabel.pack(side=LEFT, padx=5)

        self.dropDownY.current(0)
        self.dropDownY.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set())
        self.dropDownY.pack(side=LEFT, padx=5)

        self.btnStyle = ttk.Style()
        self.btnStyle.configure('my.TButton', font=controller.buttonFont)

        self.plotBtn = ttk.Button(
            self, text="plot",  command=self.plotIt, style="my.TButton")
        self.plotBtn.pack(side=LEFT, padx=5)

        self.customPlotBtn = ttk.Button(
            self, text="custom",  command=self.customPlotIt, style="my.TButton")
        self.customPlotBtn.pack(side=LEFT, padx=5)

        self.realTimePlotBtn = ttk.Button(
            self, text="RealTime",  command=self.initRealTimeParameter, style="my.TButton")
        self.realTimePlotBtn.pack(side=LEFT, padx=5)

    def updateDropDownXY(self):
        print("update", self.controller.dataName)
        self.dropDownX.config(values=self.controller.dataName)
        self.dropDownY.config(values=self.controller.dataName)

    def plotIt(self):
        graphNum = self.dropDownGraph.get()
        xValue = self.controller.data[self.dropDownX.current()]
        yValue = self.controller.data[self.dropDownY.current()]
        xTitle = self.dropDownX.get()
        yTitle = self.dropDownY.get()

        self.controller.graphFrame.plot(
            graphNum, xValue, yValue, xTitle, yTitle)

    def customPlotIt(self):
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
        self.controller.graphFrame.realTimeXIndex = self.dropDownX.current()
        self.controller.graphFrame.realTimeYIndex = self.dropDownY.current()
        self.controller.graphFrame.realTimeXTitle = self.dropDownX.get()
        self.controller.graphFrame.realTimeYTitle = self.dropDownY.get()
        self.controller.graphFrame.realTime = True
        self.controller.graphFrame.startRealTimePlotThread()
