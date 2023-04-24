
from openpyxl import Workbook
from openpyxl import load_workbook
from classes import Stats
from mapping import USERID, ACTUAL_SLEEP


stats = []

workbook2 = load_workbook(filename = "donnees_actimetres.xlsx", read_only=True)
for sheet in workbook2 : 
    stat = Stats(id = sheet[USERID].value, actual_sleep_rate = sheet[ACTUAL_SLEEP].value)
    
    stats.append(stat)
    print(stats)

workbook = Workbook();
sheet = workbook.active

sheet.append(["UserID", "actual_sleep_rate"])
for stat in stats : 
    data = [stat.id, stat.actual_sleep_rate]
    sheet.append(data)


workbook.save(filename= "test.xlsx")