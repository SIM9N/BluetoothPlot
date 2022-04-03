import serial.tools.list_ports
from tkinter import*
from tkinter import ttk, messagebox


def defocus(event):
    event.widget.master.focus_set()


LabelFrameFont = ("Courier New", "14", "bold")
labelFont = ("Courier New", "14")
dropDownFont = ("Courier New", "13")
ButtonFont = ("Courier New", "14")
textFont = ("Courier New", "11")


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
        self.dataName = []

        self.left = LeftContainer(self)
        self.left.place(relwidth=0.25, relheight=1, x=0, y=0)

        self.right = RightContainer(self)
        self.right.place(relwidth=0.75, relheight=1, x=300, y=0)


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

        self.serialPanel1 = LoggingPanel(self)
        self.serialPanel1.grid(column=0, row=1, padx=4,
                               pady=(3, 0), sticky="NESW")

        self.serialPanel2 = SerialDataFrame(self)
        self.serialPanel2.grid(column=0, row=2, padx=4,
                               pady=(3, 3), sticky="NESW")


class RightContainer(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(bg="#78AFD4", bd=3, relief="groove")


class SerialDataFrame(LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.config(labelwidget=ttk.Label(
            text="SerialDataFrame", font=LabelFrameFont, foreground="grey",
            background=self.backgroundColor), background=self.backgroundColor)

        self.textData = Text(self, wrap=NONE, font=textFont,
                             takefocus=0, bg="white", fg="black", bd=0)
        self.textData.bind("<FocusIn>", defocus)
        self.textVerticalScrollbar = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.textData.yview)
        self.textHorizontalScrollbar = ttk.Scrollbar(
            self, orient=HORIZONTAL, command=self.textData.xview
        )
        self.textData["yscroll"] = self.textVerticalScrollbar.set
        self.textData["xscroll"] = self.textHorizontalScrollbar.set

        self.textData.place(
            anchor=NW,
            x=2,
            y=0,
            relheight=0.95,
            relwidth=0.93
        )

        self.textVerticalScrollbar.place(
            anchor=NW,
            x=264,
            y=0,
            relwidth=0.05,
            relheight=0.95
        )

        self.textHorizontalScrollbar.place(
            x=2,
            y=345,
            relheight=0.05,
            relwidth=0.92
        )


class SerialPanel(LabelFrame):
    def __init__(self, master):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.config(labelwidget=ttk.Label(
            text="SerialPanel", font=LabelFrameFont, foreground="grey", background=self.backgroundColor), background=self.backgroundColor)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        # Choose a serial Port
        self.portLabel = Label(self, text="Port:", font=labelFont,
                               background=self.backgroundColor, foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.portLabel.grid(column=0, row=0, columnspan=2,
                            padx=(4, 0), sticky="WE")

        self.serialPortOptions = self.initSerialPortOptions()
        self.dropDownSerialOptions = ttk.Combobox(
            self,
            value=self.serialPortOptions,
            font=dropDownFont,
            state="readonly",
        )
        self.dropDownSerialOptions.current(0)
        self.dropDownSerialOptions.bind("<FocusIn>", defocus)
        self.dropDownSerialOptions.grid(
            column=2, row=0, columnspan=4, padx=(4, 4), sticky="WE")

        # Choose a baudrate
        self.baudrateLabel = Label(self, text="Baudrate:", font=labelFont,
                                   background=self.backgroundColor, foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.baudrateLabel.grid(column=0, row=1, columnspan=2,
                                padx=(4, 0), sticky="WE")

        self.baudrateOptions = [1800, 2400, 4800, 9600,
                                19200, 28800, 38400, 57600, 76800, 115200]
        self.dropDownBaudrateOptions = ttk.Combobox(
            self,
            value=self.baudrateOptions,
            font=dropDownFont,
            state="readonly",
        )
        self.dropDownBaudrateOptions.current(len(self.baudrateOptions) - 1)
        self.dropDownBaudrateOptions.bind("<FocusIn>", defocus)
        self.dropDownBaudrateOptions.grid(
            column=2, row=1, columnspan=4, padx=(4, 4), sticky="WE")

        btnStyle = ttk.Style()
        btnStyle.configure('my.TButton', font=ButtonFont)
        self.connectBtn = ttk.Button(
            self, text="connect", command=self.initComPort, style="my.TButton")
        self.connectBtn.grid(column=0, row=2, columnspan=3,
                             padx=(4, 4), sticky="WE")

        self.startBtn = ttk.Button(
            self, text="start", command=self.initComPort, style="my.TButton")
        self.startBtn.grid(column=3, row=2, columnspan=3,
                           padx=(4, 4), sticky="WE")

    def initSerialPortOptions(self):
        portOptions = [""]
        for onePort in serial.tools.list_ports.comports():
            portOptions.append(str(onePort).split(" ")[0])
        return portOptions

    def initComPort(self):
        try:
            if(self.connectBtn.cget("text") == "connect"):
                app.serialPort.port = self.dropDownSerialOptions.get()
                app.serialPort.baudrate = self.dropDownBaudrateOptions.get()
                app.serialPort.close()
                app.serialPort.open()
                messagebox.showinfo(
                    "Success", "Connected to " + self.dropDownSerialOptions.get())
                self.connectBtn.config(text="diconnect")
            else:
                app.serialPort.close()
                self.connectBtn.config(text="connect")
        except IOError as e:
            messagebox.showerror(
                "Error",
                "Error, can't connect to "
                + self.dropDownSerialOptions.get()
                + "\n\n"
                + "( "
                + str(e)
                + " )",
            )


class LoggingPanel(LabelFrame):

    def __init__(self, master):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.config(labelwidget=ttk.Label(
            text="LoggingPanel", font=LabelFrameFont, foreground="grey",
            background=self.backgroundColor), background=self.backgroundColor)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        btnStyle = ttk.Style()
        btnStyle.configure('my.TButton', font=ButtonFont)
        self.exportBtn = ttk.Button(
            self, text="export", command=None, style="my.TButton")
        self.exportBtn.grid(column=0, row=2, columnspan=3,
                            padx=(4, 4), sticky="WE")

        self.cleanBtn = ttk.Button(
            self, text="clean", command=None, style="my.TButton")
        self.cleanBtn.grid(column=3, row=2, columnspan=3,
                           padx=(4, 4), sticky="WE")


app = SerialPlotTool("SerialPlotTool", "1200x700")
app.mainloop()
