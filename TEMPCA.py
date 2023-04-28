
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import PatternFill
from openpyxl.styles import Font, Color, Alignment, Border, Side

from classes import Stats
from classes import ToplevelWindow, MainWindow
from mapping import FRAGMENTATION_INDEX, SLEEP_LATENCY, ACTUAL_WAKE_TIME, SLEEP_EFFICIENCY, LIGHTS_OUT, GOT_UP, TIME_IN_BED, ASSUMED_SLEEP, ACTUAL_SLEEP_TIME
from mapping import USERID, ACTUAL_SLEEP_RATE, ACTUAL_WAKE_RATE, FELL_ASLEEP, WOKE_UP

import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk

import csv
import pandas as pd
import pandastable as pt
from pandastable import Table, TableModel, config

from stats import moy, moydf, users, df, temp


import customtkinter
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


file_path = ""
filter = "O5JB"
filter2 = "24"


main_window = MainWindow()

        

def loadWorkbook(file_path):
    workbook2 = load_workbook(filename = file_path, read_only=True)
    workbook2.sheetnames
    stats = []


    #parcours des feuilles
    for sheet in workbook2 : 

    #les titres des feuilles sont au format USERID_TEMP (c'est moi qui l'ai décidé nah)
    #  --> n'ayant pas de vraibale température sur MotionWare on récupère la température de la nuit à partir du nom de la feuille
        temperaure = str(sheet.title[-2:])

    #remplissage de la classe
        stat = Stats(id = sheet[USERID].value, TEMP = temperaure, SPT=sheet[ASSUMED_SLEEP].value, TST= sheet[ACTUAL_SLEEP_TIME].value, 
                 actual_sleep_rate = sheet[ACTUAL_SLEEP_RATE].value, actual_wake_time=sheet[ACTUAL_WAKE_TIME].value, actual_wake_rate = sheet[ACTUAL_WAKE_RATE].value, 
                 TIB=sheet[TIME_IN_BED].value, sleep_efficiency=sheet[SLEEP_EFFICIENCY].value,lights_out=sheet[LIGHTS_OUT].value, fell_asleep=sheet[FELL_ASLEEP].value, 
                 sleep_latency=sheet[SLEEP_LATENCY].value ,woke_up=sheet[WOKE_UP].value, got_up=sheet[GOT_UP].value, SFI=sheet[FRAGMENTATION_INDEX].value)
    
        stats.append(stat)
      
    #print(stats)

    workbook = Workbook()
    sheet = workbook.active

#nom des en-têtes
    sheet.append(["UserID", "TEMP", "TIB", "SPT", "TST", "actual_sleep (%)", "actual_wake_time", "actual_wake (%)", "sleep_efficiency (%)", "lights_out", 
              "fell_asleep", "sleep_latency", "woke_up", "got_up", "SFI"])

#remplissage du tableau
    for stat in stats : 
        data = [stat.id, stat.TEMP, stat.TIB, stat.SPT, stat.TST, stat.actual_sleep_rate, stat.actual_wake_time, stat.actual_wake_rate,stat.sleep_efficiency,
            stat.lights_out, stat.fell_asleep, stat.sleep_latency, stat.woke_up, stat.got_up, stat.SFI]
        sheet.append(data)


#Ajustement de la largeur de la colonne en fonction de son contenu
    dims = {}
    for row in sheet.rows:
        for cell in row:
            if cell.value:
                dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))  
    for col, value in dims.items():
        sheet.column_dimensions[col].width = value

#remplissage de ligne alternatif
    gris = "e2e2e2"
    for rows in sheet.iter_rows(min_row=2, max_row=69, min_col=1, max_col=15):
        for cell in rows:
            if cell.row % 2:
                cell.fill = PatternFill(start_color=gris, end_color=gris,fill_type = "solid")

#code couleur pour la température
    color_scale_rule = ColorScaleRule(end_type="num",
                                  end_value=32,
                                  end_color="e67d59",  # Rouge
                                  mid_type="num",
                                  mid_value=24,
                                  mid_color="9edd87",  # vert
                                  start_type="num",
                                  start_value=16,
                                  start_color="c3d2ff")  # bleu
    sheet.conditional_formatting.add("B2:B69", color_scale_rule)


#filtres
    sheet.auto_filter.ref = sheet.dimensions

#epingle la première ligne
    sheet.freeze_panes = "B2"

    filter = StringVar()
    filter.set(moy)

    def optionmenu_user_callback(choice):
        filtrage= df["UserID"] == choice
        print(filtrage)
        filter.set (str(df[filtrage]))
        newdf = df[filtrage]
        fillTable(newdf)
        print(newdf)
        
    
    def optionmenu_temp_callback(choice):
        filtrage= (df["TEMP"].astype('string') == choice)
        filter.set (df.loc[df["TEMP"] == "16"])
        newdf = df[filtrage]
        print(df[filtrage])
        fillTable(newdf)


    workbook.save(filename= "test.xlsx")
    df = pd.DataFrame(pd.read_excel("test.xlsx"))

    buttonSelectionFichier.destroy()




    style = ttk.Style()
    
    style.theme_use("default")
    
    style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="white",
                            rowheight=25,
                            fieldbackground="#343638",
                            bordercolor="#343638",
                            borderwidth=0)
    style.map('Treeview', background=[('selected', '#565b5e')])
    
    style.configure("Treeview.Heading",
                            background="#52a57c",
                            foreground="white",
                            relief="flat")
    style.map("Treeview.Heading", background=[('active', '#52a57c')])




    def fillTable(newdf):
        
        df_list=list(df)
        df_rset=newdf.round(2).to_numpy().tolist()

        df_tree = ttk.Treeview(main_window.tabView.tab("Prout"), columns=df_list)
        for i in df_tree.get_children():
            df_tree.delete(i)
        df_tree["show"] = "headings"
        df_tree.place(relx=.5, rely=.35, anchor="center")

        for i in df_list:
            df_tree.column(i,width=75,anchor='c')
            df_tree.heading(i,text=i)
        for dt in df_rset:
            v=[r for r in dt]
            df_tree.insert('','end', values=v)
    
    fillTable(df)


    optionmenu1_var = customtkinter.StringVar(value=users[1])
    optionmenu2_var = customtkinter.StringVar(value=temp[0])

    optionmenu_user = customtkinter.CTkOptionMenu(master=main_window.tabView.tab("Prout"), dynamic_resizing=False, values = users, command=optionmenu_user_callback, variable=optionmenu1_var)
    optionmenu_user.place(relx=0.1, rely=.075, anchor="center")
    optionmenu_2 = customtkinter.CTkOptionMenu(master=main_window.tabView.tab("Prout"), dynamic_resizing=False, values = temp, command=optionmenu_temp_callback, variable=optionmenu2_var)
    optionmenu_2.place(relx=.5, rely=.075, anchor="center")
    optionmenu_2 = customtkinter.CTkOptionMenu(master=main_window.tabView.tab("Prout"), dynamic_resizing=False, values = users, command=optionmenu_user_callback, variable=optionmenu1_var)
    optionmenu_2.place(relx=0.9, rely=.075, anchor="center")
    

    
 
    main_window.label_stats = customtkinter.CTkLabel(main_window.tabView.tab("Prout"), textvariable= filter, font=customtkinter.CTkFont(size=10, weight="bold"))
    main_window.label_stats.place(relx=.5, rely=.7, anchor="center")

def UploadAction():
    file_path = filedialog.askopenfilename()
    if file_path is not None:
        print (file_path)
        loadWorkbook(file_path)
        textSelectionFichier.set("Filtrage par sujet")

textSelectionFichier = StringVar()
textSelectionFichier.set("Sélectionner le fichier à traiter")
main_window.labelSelectionFichier = customtkinter.CTkLabel(master = main_window.tabView.tab("Prout"), textvariable = textSelectionFichier, font=customtkinter.CTkFont(size=40, weight="bold"))
main_window.labelSelectionFichier.place(relx=.5, rely=.3, anchor="center")
buttonSelectionFichier = customtkinter.CTkButton(master = main_window.tabView.tab("Prout"), text='Sélectionner...', command=UploadAction, width=200, height=50, font=customtkinter.CTkFont(size=20))
buttonSelectionFichier.place(relx=.5, rely=.6, anchor="center")




main_window.mainloop()

