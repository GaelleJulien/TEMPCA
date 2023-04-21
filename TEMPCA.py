
from openpyxl import Workbook
from openpyxl import load_workbook


workbook = load_workbook(filename = "donnees_actimetres.xlsx")
sheet = workbook.active

print(sheet["B3"].value)


workbook.save(filename="test.xlsx")

