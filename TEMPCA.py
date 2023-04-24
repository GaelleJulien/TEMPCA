
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font, Color, Alignment, Border, Side

from classes import Stats
from mapping import USERID, ACTUAL_SLEEP_RATE, ACTUAL_WAKE_RATE, FELL_ASLEEP, WOKE_UP, SLEEP_EFFICIENCY, LIGHTS_OUT, GOT_UP


stats = []

workbook2 = load_workbook(filename = "donnees_actimetres.xlsx", read_only=True)
workbook2.sheetnames
for sheet in workbook2 : 

    #les titres des feuilles si=ont au format USERID_TEMP
    temp = int(sheet.title[-2:])
    stat = Stats(id = sheet[USERID].value,temp = temp ,actual_sleep_rate = sheet[ACTUAL_SLEEP_RATE].value, actual_wake_rate = sheet[ACTUAL_WAKE_RATE].value,  
                 sleep_efficiency=sheet[SLEEP_EFFICIENCY].value,lights_out=sheet[LIGHTS_OUT].value, fell_asleep=sheet[FELL_ASLEEP].value, woke_up=sheet[WOKE_UP].value, got_up=sheet[GOT_UP].value)
    
    stats.append(stat)
    #print(stats)

workbook = Workbook();
sheet = workbook.active

sheet.append(["UserID","temperature", "actual_sleep (%)", "actual_wake (%)", "sleep_efficiency (%)", "lights_out","fell_asleep", "woke_up", "got_up"])
for stat in stats : 
    data = [stat.id, stat.temp, stat.actual_sleep_rate, stat.actual_wake_rate,stat.sleep_efficiency,stat.lights_out, stat.fell_asleep, stat.woke_up, stat.got_up]
    sheet.append(data)


sheet
dims = {}
for row in sheet.rows:
    for cell in row:
        if cell.value:
             dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))    
for col, value in dims.items():
    sheet.column_dimensions[col].width = value
    
workbook.save(filename= "test.xlsx")