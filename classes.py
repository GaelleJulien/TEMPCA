from dataclasses import dataclass
import datetime


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
    fragmentation_index : str



class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Pop up éclatée au sol")
        self.label.pack(padx=20, pady=20)