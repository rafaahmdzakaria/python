import tkinter as tk
from time import strftime

root = tk.Tk()
root.title("Digital Clock")
root.geometry("750x220")    
root.resizable(False, False)

def time():
    string = strftime('%H:%M:%S %p \n %D')
    label.config(text=string)
    label.after(1000, time)

label = tk.Label(
    root,
    font=("ds-digital", 80),
    background='black',
    foreground='white',
    justify='center'
)
label.pack(fill='both', expand=True)

time()
root.mainloop()
