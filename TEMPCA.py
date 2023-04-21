
from openpyxl import Workbook
from openpyxl import load_workbook
from classes import Stats
from mapping import USERID, ACTUAL_SLEEP



workbook = load_workbook(filename = "donnees_actimetres.xlsx", read_only=True)
for sheet in workbook : 
    stats = []
    stat = Stats(id = sheet[USERID].value, actual_sleep_rate = sheet[ACTUAL_SLEEP].value)
    stats.append(stat)
    print(stats)
