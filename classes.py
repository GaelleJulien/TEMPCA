from dataclasses import dataclass
import datetime



@dataclass
class Stats :
    id : str
    temp : int
    actual_sleep_rate : float
    actual_wake_rate : float
    sleep_efficiency : float
    lights_out : datetime
    fell_asleep : datetime
    woke_up : datetime
    got_up : datetime

