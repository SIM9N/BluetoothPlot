from pyexpat.errors import XML_ERROR_ENTITY_DECLARED_IN_PE
from tkinter import*
from tkinter import ttk
import matplotlib.pyplot as plt

LabelFrameFont = ("Courier New", "14", "bold")
dropDownFont = ("Courier New", "13")
labelFont = ("Courier New", "14")
ButtonFont = ("Courier New", "14")


def defocus(event):
    event.widget.master.focus_set()


class GraphControlPanel(LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        # self.backgroundColor = "red"
        self.config(labelwidget=ttk.Label(
            text="GraphControlPanel", font=LabelFrameFont, foreground="grey", background=self.backgroundColor), background=self.backgroundColor)

        self.dropDownGraph = ttk.Combobox(
            self,
            value=["graph1", "graph2", "graph3", "graph4"],
            font=dropDownFont,
            state="readonly",
            width=7,
        )
        self.graphLabel = Label(
            self, text="plot", font=labelFont, background=self.backgroundColor, foreground="black", border=2, relief="groove", padx=10, pady=5
        )
        self.graphLabel.pack(side=LEFT, padx=5)

        self.dropDownGraph.current(0)
        self.dropDownGraph.bind("<FocusIn>", defocus)
        self.dropDownGraph.pack(side=LEFT, padx=5)

        self.dropDownX = ttk.Combobox(
            self,
            value=master.master.dataName,
            font=dropDownFont,
            state="readonly",
            width=10,
        )
        self.xLabel = Label(self, text="X", font=labelFont, background=self.backgroundColor,
                            foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.xLabel.pack(side=LEFT, padx=5)

        self.dropDownX.current(0)
        self.dropDownX.bind("<FocusIn>", defocus)
        self.dropDownX.pack(side=LEFT, padx=5)

        self.dropDownY = ttk.Combobox(
            self,
            value=master.master.dataName,
            font=dropDownFont,
            state="readonly",
            width=10,
        )

        self.yLabel = Label(self, text="Y", font=labelFont, background=self.backgroundColor,
                            foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.yLabel.pack(side=LEFT, padx=5)

        self.dropDownY.current(0)
        self.dropDownY.bind("<FocusIn>", defocus)
        self.dropDownY.pack(side=LEFT, padx=5)

        self.btnStyle = ttk.Style()
        self.btnStyle.configure('my.TButton', font=ButtonFont)

        self.plotBtn = ttk.Button(
            self, text="plot",  command=self.plotIt, style="my.TButton")
        self.plotBtn.pack(side=LEFT, padx=5)

        self.customPlotBtn = ttk.Button(
            self, text="custom",  command=self.customPlotIt, style="my.TButton")
        self.customPlotBtn.pack(side=LEFT, padx=5)

        self.realTimePlotBtn = ttk.Button(
            self, text="realTime",  command=self.initRealTimeParameter, style="my.TButton")
        self.realTimePlotBtn.pack(side=LEFT, padx=5)

    def updateDropDownXY(self):
        print("update", self.master.master.dataName)
        self.dropDownX.config(values=self.master.master.dataName)
        self.dropDownY.config(values=self.master.master.dataName)

    def plotIt(self):
        graphNum = self.dropDownGraph.get()
        xValue = self.master.master.data[self.dropDownX.current()]
        yValue = self.master.master.data[self.dropDownY.current()]
        xTitle = self.dropDownX.get()
        yTitle = self.dropDownY.get()

        self.master.graphFrame.plot(graphNum, xValue, yValue, xTitle, yTitle)

    def customPlotIt(self):
        plt.plot(
            self.master.master.data[self.dropDownX.current()],
            self.master.master.data[self.dropDownY.current()],
            color="#444444",
            linestyle="--",
            label="label",
        )
        plt.title("cutomGraph")
        plt.xlabel(self.dropDownX.get())
        plt.ylabel(self.dropDownY.get())
        plt.show()

    def initRealTimeParameter(self):
        self.master.graphFrame.realTimeXIndex = self.dropDownX.current()
        self.master.graphFrame.realTimeYIndex = self.dropDownY.current()
        self.master.graphFrame.realTimeXTitle = self.dropDownX.get()
        self.master.graphFrame.realTimeYTitle = self.dropDownY.get()
        self.master.graphFrame.realTime = True
