import threading
from time import sleep
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import*
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")


class GraphFrame(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.controller = controller
        # self.backgroundColor = "red"
        self.config(labelwidget=ttk.Label(
            text="GraphFrame", font=controller.labelFrameFont, foreground="grey", background=self.backgroundColor), background=self.backgroundColor)

        self.fig = Figure(figsize=(0.1, 0.1), dpi=100)
        self.rt = self.fig.add_subplot(111)
        self.ax1 = self.fig.add_subplot(221)
        self.ax2 = self.fig.add_subplot(222)
        self.ax3 = self.fig.add_subplot(223)
        self.ax4 = self.fig.add_subplot(224)
        self.ax1.set_visible(False)
        self.ax2.set_visible(False)
        self.ax3.set_visible(False)
        self.ax4.set_visible(False)

        self.realTimeView = True
        self.realTime = False
        self.realTimeXIndex = 0
        self.realTimeYIndex = 0
        self.realTimeXTitle = ""
        self.realTimeYTitle = ""
        self.realTimeThread = None

        class Toolbar(NavigationToolbar2Tk):
            def set_message(self, s):
                pass

        self.graphCanvas = FigureCanvasTkAgg(self.fig, self)
        self.graphCanvas.draw()
        self.graphToolBar = Toolbar(self.graphCanvas, self, pack_toolbar=False)
        self.graphToolBar.update()

        self.graphCanvas.get_tk_widget().place(relwidth=1, relheight=0.89, x=0, y=0)
        self.graphToolBar.place(relwidth=0.95, relheight=0.1, x=5, y=535)

        self.btnStyle = ttk.Style()
        self.btnStyle.configure('my.TButton', font=controller.buttonFont)
        self.toggleViewPlotBtn = ttk.Button(
            self, text="toggleView",  command=self.toggleView, style="my.TButton")
        self.toggleViewPlotBtn.place(x=750, y=550)

    def plot(self, graphNum, xValue, yValue, xTitle, yTitle):
        if graphNum == "graph1":
            self.ax1.cla()
            self.ax1.plot(
                xValue,
                yValue,
                color="#444444",
                linestyle="--",
                label="label",
            )

            self.ax1.set_title(yTitle + " - " + xTitle)
            self.ax1.set_xlabel(xTitle)
            self.ax1.set_ylabel(yTitle)

        if graphNum == "graph2":
            self.ax2.cla()
            self.ax2.plot(xValue, yValue)
            self.ax2.set_title(yTitle + " - " + xTitle)
            self.ax2.set_xlabel(xTitle)
            self.ax2.set_ylabel(yTitle)

        if graphNum == "graph3":
            self.ax3.cla()
            self.ax3.plot(xValue, yValue)
            self.ax3.set_title(yTitle + " - " + xTitle)
            self.ax3.set_xlabel(xTitle)
            self.ax3.set_ylabel(yTitle)

        if graphNum == "graph4":
            self.ax4.cla()
            self.ax4.plot(xValue, yValue)
            self.ax4.set_title(yTitle + " - " + xTitle)
            self.ax4.set_xlabel(xTitle)
            self.ax4.set_ylabel(yTitle)
        self.fig.tight_layout()
        self.graphCanvas.draw()

    def startRealTimePlotThread(self):
        if not isinstance(self.realTimeThread, threading.Thread):
            self.realTimeThread = threading.Thread(target=self.realTimePlot)
            self.realTimeThread.start()
            print('realTimePlotThread started')

    def realTimePlot(self):
        while self.realTime:
            sleep(0.1)
            if self.controller.started and not self.controller.appendingData:
                self.rt.cla()
                self.rt.scatter(
                    self.controller.data[self.realTimeXIndex],
                    self.controller.data[self.realTimeYIndex],
                    color="#444444",
                    label="label",
                )

                self.rt.set_title(self.realTimeYTitle +
                                  " - " + self.realTimeXTitle)
                self.rt.set_xlabel(self.realTimeXTitle)
                self.rt.set_ylabel(self.realTimeYTitle)

                self.graphCanvas.draw()

        print('realTimePlotThread terminated')

    def toggleView(self):
        self.realTimeView = not self.realTimeView
        self.ax1.set_visible(not self.realTimeView)
        self.ax2.set_visible(not self.realTimeView)
        self.ax3.set_visible(not self.realTimeView)
        self.ax4.set_visible(not self.realTimeView)
        self.rt.set_visible(self.realTimeView)
        self.graphCanvas.draw()
