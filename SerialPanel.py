from doctest import master
from tkinter import *
import serial.tools.list_ports
from tkinter import ttk, messagebox

LabelFrameFont = ("Courier New", "14", "bold")
labelFont = ("Courier New", "14")
dropDownFont = ("Courier New", "13")
ButtonFont = ("Courier New", "14")


def defocus(event):
    event.widget.master.focus_set()


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
        btnStyle.configure('my.TButton', font=ButtonFont, )
        self.connectBtn = ttk.Button(
            self, text="connect", command=self.initComPort, style="my.TButton")
        self.connectBtn.grid(column=0, row=2, columnspan=3,
                             padx=(4, 4), sticky="WE")

        self.startBtn = ttk.Button(
            self, text="start", command=self.startAppend, style="my.TButton", state="disable")
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
                self.master.master.serialPort.port = self.dropDownSerialOptions.get()
                self.master.master.serialPort.baudrate = self.dropDownBaudrateOptions.get()
                self.master.master.serialPort.close()
                self.master.master.serialPort.open()
                self.connectBtn.config(text="diconnect")
                messagebox.showinfo(
                    "Success", "Connected to " + self.dropDownSerialOptions.get())
            else:
                self.master.master.serialPort.close()
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

    def startAppend(self):
        if(self.startBtn.cget("text") == "start"):
            print("start appending")
            self.master.master.started = True
            self.startBtn.config(text="stop")
        else:
            print("stop appending")
            self.master.master.started = False
            self.startBtn.config(text="start")
