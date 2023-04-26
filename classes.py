from dataclasses import dataclass
import datetime
from tkinter import *


import customtkinter



@dataclass
class Stats :
    id : str
    temp : int
    time_in_bed : datetime
    assumed_sleep : datetime
    actual_sleep_time : datetime
    actual_sleep_rate : float
    actual_wake_time : datetime
    actual_wake_rate : float
    sleep_efficiency : float
    lights_out : datetime
    fell_asleep : datetime
    sleep_latency : datetime
    woke_up : datetime
    got_up : datetime
    fragmentation_index : float



class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x300")
        self.title("Pop up")

        self.label = customtkinter.CTkLabel(self, text="Pop up éclatée au sol")
        self.label.pack(padx=20, pady=20)
        self.after(20, self.lift)

        

class MainWindow(customtkinter.CTk) : 
    def __init__(self):
        super().__init__()

        self.title("Gaëlle règne suprême parmi les mortels")
        self.geometry(f"{1100}x{580}")

        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Bip boup", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not secondary_window.toplevel_window.winfo_exists():
            secondary_window = ToplevelWindow(self)
            secondary_window.label = customtkinter.CTkLabel(secondary_window, text="Mouhahaha tremblez mortels")
            secondary_window.label.pack(padx=20, pady=20)
            buttonAfficherTable = customtkinter.CTkButton(master = secondary_window, text='Afficher les données')
            buttonAfficherTable.place(relx = 0.5, rely=0.7, anchor=CENTER)
        else : 
            secondary_window.toplevel_window.focus()  # if window exists focus it

