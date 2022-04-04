import threading
from tkinter import*
from tkinter import ttk, messagebox, filedialog
from turtle import left
from openpyxl import Workbook, load_workbook
import datetime


class LoggingPanel(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.config(labelwidget=ttk.Label(
            text="LoggingPanel", font=controller.labelFrameFont, foreground="grey",
            background=self.backgroundColor), background=self.backgroundColor)
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        btnStyle = ttk.Style()
        btnStyle.configure('my.TButton', font=controller.buttonFont)

        self.filename = ""
        self.printNote = True

        self.noteLabel = Label(self, text="Note:", font=controller.labelFont,
                               background=self.backgroundColor, foreground="black", border=2, relief="groove", padx=10, pady=5)
        self.noteLabel.grid(column=0, row=0, columnspan=2,
                            padx=(4, 0), pady=0, sticky="WE")

        self.note = Entry(self, font=('Arial', 20),
                          borderwidth=0, highlightthickness=2, highlightbackground="grey", highlightcolor="grey")
        self.note.grid(column=2, row=0, columnspan=6,
                       padx=(4, 4), pady=0, sticky="WE")

        self.openBtn = ttk.Button(
            self, text="open", command=self.openExcelFile, style="my.TButton")
        self.openBtn.place(relwidth=0.3, relheight=0.3, x=4, y=55)

        self.exportBtn = ttk.Button(
            self, text="export", command=self.export2xlsx, style="my.TButton")
        self.exportBtn.place(relwidth=0.3, relheight=0.3, x=120, y=55)

    def export2xlsx(self):
        try:
            wb = load_workbook(self.filename)
        except:
            wb = Workbook()
            wb.create_sheet("all")
            wb.create_sheet("once")
            self.filename = "./excel/"+datetime.datetime.now().strftime("%d-%m-%y %H:%M")+".xlsx"

        ws = wb["all"]
        ws.append(["note", self.note.get()])
        ws.append(self.controller.dataName)

        for i in range(len(self.controller.data[0])-1):
            ws.append(self.controller.data[j][i+1]
                      for j in range(len(self.controller.data)))

        ws.append([])
        wb.save(self.filename)
        print("saved " + self.filename + ".xlsx")

    def openExcelFile(self):
        self.filename = filedialog.askopenfilename(
            initialdir="./excel", title="Select a excel file", filetypes=(("all", "."), ("xlsx", "*.xlsx")))

    def autoExport(self, cmd):
        packetArray = self.controller.packetString.strip("\n").split("-")
        try:
            wb = load_workbook(self.filename)
        except:
            wb = Workbook()
            wb.create_sheet("all")
            wb.create_sheet("once")
            self.filename = "./excel/"+datetime.datetime.now().strftime("%d-%m-%y %H:%M")+".xlsx"

        ws = wb["once"]
        if self.printNote:
            ws.append(["note", self.note.get()])
        if cmd == "save":
            packetArray.pop(0)
            print(packetArray)
            ws.append(packetArray)
            wb.save(self.filename)
            self.printNote = False
        if cmd == "end":
            ws.append([])
            wb.save(self.filename)
            self.printNote = True
            print("saved " + self.filename + ".xlsx")
