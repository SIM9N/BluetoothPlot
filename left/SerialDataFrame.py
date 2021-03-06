from tkinter import*
from tkinter import ttk


class SerialDataFrame(LabelFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.backgroundColor = master.backgroundColor
        self.controller = controller
        self.config(labelwidget=ttk.Label(
            text="SerialDataFrame", font=controller.labelFrameFont, foreground="grey",
            background=self.backgroundColor), background=self.backgroundColor)

        self.textData = Text(self, wrap=NONE, font=controller.textFont,
                             takefocus=0, bg="white", fg="black", bd=0)
        self.textData.bind(
            "<FocusIn>", lambda event: event.widget.master.focus_set())
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
            relheight=0.98,
            relwidth=0.93
        )

        self.textVerticalScrollbar.place(
            anchor=NW,
            x=264,
            y=0,
            relwidth=0.05,
            relheight=0.98
        )

        self.textHorizontalScrollbar.place(
            x=2,
            y=390,
            relheight=0.05,
            relwidth=0.92
        )

        self.menu = Menu(self.textData, tearoff=False)
        self.menu.add_command(label="clean", command=self.cleanData)
        self.menu.add_command(label="export", command=self.exportData)

        self.textData.bind("<Button-2>", self.popupMenu)

    def cleanData(self):
        self.textData.delete(1.0, END)

    def exportData(self):
        pass

    def popupMenu(self, e):
        self.menu.tk_popup(e.x_root, e.y_root)

    def insert2Text(self, string):
        self.textData.insert("end", string)
        self.textData.see(END)
