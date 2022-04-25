from tkinter import *
import serial.tools.list_ports
from tkinter import ttk, messagebox


class SerialPanel(LabelFrame):
    column1_x = 5
    row1_y = 7
    row2_y = 52

    relHeight = 0.35

    def __init__(self, master, controller):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.controller = controller
        self.config(
            labelwidget=ttk.Label(
                text="SerialPanel",
                font=controller.labelFrameFont,
                foreground="grey",
                background=self.backgroundColor,
            ),
            background=self.backgroundColor,
        )

        # Choose a serial Port
        self.portLabel = Label(
            self,
            text="Port:",
            font=controller.labelFont,
            background=self.backgroundColor,
            foreground="black",
            border=2,
            relief="groove",
            padx=10,
            pady=5,
        )
        self.portLabel.place(
            relwidth=0.2, relheight=self.relHeight, x=self.column1_x, y=self.row1_y
        )

        self.serialPortOptions = self.initSerialPortOptions()
        self.dropDownSerialOptions = ttk.Combobox(
            self,
            value=self.serialPortOptions,
            font=controller.dropDownFont,
            state="readonly",
        )
        self.dropDownSerialOptions.current(0)
        self.dropDownSerialOptions.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set()
        )
        self.dropDownSerialOptions.place(
            relwidth=0.71, relheight=self.relHeight, x=70, y=self.row1_y
        )

        # Choose a baudrate
        self.baudrateLabel = Label(
            self,
            text="Baudrate:",
            font=controller.labelFont,
            background=self.backgroundColor,
            foreground="black",
            border=2,
            relief="groove",
            padx=10,
            pady=5,
        )
        self.baudrateLabel.place(
            relwidth=0.3, relheight=self.relHeight, x=self.column1_x, y=self.row2_y
        )

        self.baudrateOptions = [
            1800,
            2400,
            4800,
            9600,
            19200,
            28800,
            38400,
            57600,
            76800,
            115200,
        ]
        self.dropDownBaudrateOptions = ttk.Combobox(
            self,
            value=self.baudrateOptions,
            font=controller.dropDownFont,
            state="readonly",
        )
        self.dropDownBaudrateOptions.current(len(self.baudrateOptions) - 1)
        self.dropDownBaudrateOptions.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set()
        )
        self.dropDownBaudrateOptions.place(
            relwidth=0.30, relheight=self.relHeight, x=95, y=self.row2_y
        )

        btnStyle = ttk.Style()
        btnStyle.configure(
            "my.TButton",
            font=controller.buttonFont,
        )
        self.connectBtn = ttk.Button(
            self, text="connect", command=self.initComPort, style="my.TButton"
        )
        self.connectBtn.place(
            relwidth=0.30, relheight=self.relHeight, x=185, y=self.row2_y
        )

        # self.startBtn = ttk.Button(
        #     self, text="start", command=self.startAppend, style="my.TButton", state="disable")
        # self.startBtn.grid(column=3, row=2, columnspan=3,
        #                    padx=(4, 4), sticky="WE")

    def initSerialPortOptions(self):
        portOptions = [""]
        for onePort in serial.tools.list_ports.comports():
            portOptions.append(str(onePort).split(" ")[0])
        return portOptions

    def initComPort(self):
        try:
            if self.connectBtn.cget("text") == "connect":
                self.controller.serialPort.port = self.dropDownSerialOptions.get()
                self.controller.serialPort.baudrate = self.dropDownBaudrateOptions.get()
                self.controller.serialPort.close()
                self.controller.serialPort.open()
                self.connectBtn.config(text="disconnect")
                self.controller.dataName = [""]
                self.controller.data = []
                self.controller.graphControlPanel.updateDropDownXY()
                self.dataNameInited = False
                messagebox.showinfo(
                    "Success", "Connected to " + self.dropDownSerialOptions.get()
                )
                self.controller.startReadingThread()
            else:
                self.controller.serialPort.close()
                self.connectBtn.config(text="connect")
                self.controller.graphFrame.realTime = False
                saveB4Disconnect = messagebox.askquestion(
                    "Exit Application",
                    "Do you want to save the data before disconnect?",
                )
                if saveB4Disconnect == "yes":
                    self.controller.loggingPanel.export2xlsx()

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
