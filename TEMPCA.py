
from openpyxl import Workbook
from openpyxl import load_workbook
from classes import Stats
from mapping import USERID, SLEEPRATE



workbook = load_workbook(filename = "donnees_actimetres.xlsx", read_only=True)
sheet = workbook.active


stats = []


stat = Stats(id = sheet[USERID].value, actualSleepRate = sheet[SLEEPRATE].value)
stats.append(stat)
print(stat)
