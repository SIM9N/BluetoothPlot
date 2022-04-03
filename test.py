from curses import window
from tkinter import *
import serial.tools.list_ports
import functools

avaPorts = serial.tools.list_ports.comports()
serialObj = serial.Serial()

root = Tk()
root.title("BluetoothPlot")
root.geometry("1200x700")
root.config(bg="grey")

frame = Frame(root)
frame.config(bg="#bbc1c8")
frame.place(relheight=1, relwidth=1, x= 0 ,y=0)

root.mainloop()
