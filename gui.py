import tkinter as tk
from tkinter import filedialog


def UploadAction():
    file_path = filedialog.askopenfilename()
    print(file_path)
    if file_path is not None:
        pass



window = tk.Tk()
frame = tk.Frame()
frame.pack()

button = tk.Button(window, text='Open', command=UploadAction)
button.pack()

greeting = tk.Label(text="Hello there")
zoneTexte = tk.Entry()

greeting.pack()

reponse = zoneTexte.get()
greeting = tk.Label(text= reponse)


zoneTexte.pack()

window.mainloop()