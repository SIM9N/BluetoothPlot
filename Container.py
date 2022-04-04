from tkinter import *


class LeftContainer(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.backgroundColor = "#E0FFFF"
        self.config(bg=self.backgroundColor, bd=3, relief="groove")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=6)


class RightContainer(Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.backgroundColor = "#78AFD4"
        self.backgroundColor = "white"
        self.config(bg=self.backgroundColor, bd=3, relief="groove")
