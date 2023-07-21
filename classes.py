from dataclasses import dataclass
import datetime
from tkinter import *

from pandastable import Table, TableModel, config

import pandas as pd
import customtkinter



@dataclass
class Stats :
    id : str
    NUIT : str
    TIB : datetime
    SPT : datetime
    TST : datetime
    actual_sleep_rate : float
    actual_wake_time : datetime
    actual_wake_rate : float
    sleep_efficiency : float
    lights_out : datetime
    fell_asleep : datetime
    sleep_latency : datetime
    woke_up : datetime
    got_up : datetime
    SFI : float
    activity : list
    sleep_bouts : int
    wake_bouts : int
    immobile_bouts : int
    mean_immobile_bouts : datetime
    mean_sleep_bouts : datetime
    mean_wake_bouts : datetime
    



class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x300")
        self.title("Pop up")

        self.label = customtkinter.CTkLabel(self, text="Pop up éclatée au sol")
        self.label.pack(padx=(20,20), pady=20)
        self.after(20, self.lift)

        

class MainWindow(customtkinter.CTk) : 
    def __init__(self):
        super().__init__()

        self.title("Gaëlle règne suprême parmi les mortels")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0,1,4), weight=1)


        

        self.labelSelectionFichier = customtkinter.CTkLabel(master = self, text = "Sélectionner le fichier à traiter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.labelSelectionFichier.place(relx = 0.5, rely=0.3, anchor=CENTER)
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=12, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="MENU", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Génération de fichier", command=self.open_toplevel)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=9, column=0, padx=20, pady=10)

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        self.toplevel_window = None

        self.tabView = customtkinter.CTkTabview(self, corner_radius=0)
        self.tabView.grid(row=0, column=1,padx=(20, 20), pady=(10, 10), sticky=E+W+N+S)
        self.tabView.grid_columnconfigure(1, weight=1)
        self.tabView.grid_rowconfigure(1, weight=1)


        self.tabView.add("Données")
        self.tabView.add("Stats")
        self.tabView.tab("Stats").grid_columnconfigure(1, weight=1)
        self.tabView.tab("Stats").grid_rowconfigure(4, weight=1)

        self.tabView.add("Découpage nuit")
        self.tabView.tab("Découpage nuit").grid_columnconfigure(1, weight=1)
        self.tabView.tab("Découpage nuit").grid_rowconfigure(4, weight=1)


        



    def open_toplevel(self):
        if self.toplevel_window is None or not secondary_window.toplevel_window.winfo_exists():
            secondary_window = ToplevelWindow(self)
            secondary_window.label = customtkinter.CTkLabel(secondary_window, text="Mouhahaha tremblez mortels")
            secondary_window.label.pack(padx=20, pady=20)
            buttonAfficherTable = customtkinter.CTkButton(master = secondary_window, text='Afficher les données')
            buttonAfficherTable.place(anchor=CENTER)
            buttonAfficherTable.pack()
        else : 
            secondary_window.toplevel_window.focus()  # if window exists focus it

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
