import tkinter as tk

window = tk.Tk()
#filename = tk.filedialog.askopenfilename()
label = tk.Label(text="Enter the amount of bits to use")
label.pack()
bits = tk.Entry()
bits.pack()

window.mainloop()
print(bits)