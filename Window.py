import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import Mima

def main():
    window = tk.Tk()
    window.title("File Picker")
    window.geometry("300x100")
    window.resizable(False, False)
    window.configure(background="black")
    ttk.Button(window, text="Pick a file", command=lambda: pick()).pack()
    window.mainloop()

def pick():
    filename = fd.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Mima code files","*.mima"),("all files","*.*")))
    Mima.readFile(filename)