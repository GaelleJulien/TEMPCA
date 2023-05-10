
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import PatternFill
from openpyxl.chart import Reference, LineChart
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

from stats import moy, moydf, users, df, temp, tri, triSE

from PIL import ImageTk, Image



import customtkinter
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


file_path = ""

activityDonnees = []


main_window = MainWindow()



def ajouter_point(heure, valeur):
    activityDonnees.append([heure, valeur])
        

def loadWorkbook(file_path):
    workbook2 = load_workbook(filename = file_path)
    workbook2.sheetnames
    stats = []
    selected_users=[]
    selected_temps=[]



    #parcours des feuilles
    for sheet in workbook2 : 
    
        activityDonnees = []

        df2 = pd.read_excel(file_path, sheet.title, skiprows=18)
        heures = df2['Time']
        valeurs = df2['Activity']
        for i in range(len(heures)):
            heure = heures[i]
            valeur = valeurs[i]
            activityDonnees.append([heure, valeur])


        
        # x_axis = df2["Time"].values
        # fig = df3.plot(x="Time", y = "Activity").get_figure()
        # fig.savefig("testPlot2.png")

        
        #les titres des feuilles sont au format USERID_TEMP (c'est moi qui l'ai décidé nah)
        #  --> n'ayant pas de vraibale température sur MotionWare on récupère la température de la nuit à partir du nom de la feuille
        temperaure = str(sheet.title[-2:])
            #remplissage de la classe
        stat = Stats(id = sheet[USERID].value, TEMP = temperaure, SPT=sheet[ASSUMED_SLEEP].value, TST= sheet[ACTUAL_SLEEP_TIME].value, 
                 actual_sleep_rate = sheet[ACTUAL_SLEEP_RATE].value, actual_wake_time=sheet[ACTUAL_WAKE_TIME].value, actual_wake_rate = sheet[ACTUAL_WAKE_RATE].value, 
                 TIB=sheet[TIME_IN_BED].value, sleep_efficiency=sheet[SLEEP_EFFICIENCY].value,lights_out=sheet[LIGHTS_OUT].value, fell_asleep=sheet[FELL_ASLEEP].value, 
                 sleep_latency=sheet[SLEEP_LATENCY].value ,woke_up=sheet[WOKE_UP].value, got_up=sheet[GOT_UP].value, SFI=sheet[FRAGMENTATION_INDEX].value, activity=activityDonnees)
    
        stats.append(stat)

        heures = []
        valeurs = []


    sheet = workbook2.active


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


    def optionmenu_triSFI_callback(choice):
        if(choice == tri[0]):
            newdf = df
        if(choice == tri[1]): 
            newdf = df.sort_values(by = "SFI")
        if(choice == tri[2]):
            newdf = df.sort_values(by = "SFI", ascending=False)

        fillTable(newdf, "Prout"), 
        
    
    def optionmenu_triSE_callback(choice):

        if(choice == triSE[0]):
            newdf = df
        if(choice == triSE[1]): 
            newdf = df.sort_values(by = "sleep_efficiency (%)")
        if(choice == triSE[2]): 
            newdf = df.sort_values(by = "sleep_efficiency (%)", ascending=False)
        fillTable(newdf, "Prout")



    def checkbox_user_callback():
        if(checkbox_var_users.get() in selected_users):
            selected_users.remove(checkbox_var_users.get())
            print(selected_users)
            if(selected_temps != []):
                if(selected_users == []) :
                    filtrage = (df["TEMP"].astype(str).isin(selected_temps)) 
                    newdf_users = df[filtrage]
                else :
                    filtrage= (df["UserID"].isin(selected_users) & df["TEMP"].astype(str).isin(selected_temps))
                    newdf_users = df[filtrage]

            else : 
                if(selected_users == []) :
                    newdf_users = df
                else : 
                    filtrage= (df["UserID"].isin(selected_users))
                    newdf_users = df[filtrage]
            
        else : 
            selected_users.append(checkbox_var_users.get())
            print(selected_users)
            if(selected_temps != []):
                filtrage= (df["UserID"].isin(selected_users) & df["TEMP"].astype(str).isin(selected_temps))
            else : 
                filtrage= (df["UserID"].isin(selected_users))

            newdf_users = df[filtrage]
        
        fillTable(newdf_users, "Prout")



    def checkbox_temp_callback():
        print(checkbox_var_temp.get())
        if(checkbox_var_temp.get() in selected_temps):
            selected_temps.remove(checkbox_var_temp.get())
            if(selected_users != []):
                if(selected_temps == []) :
                    filtrage = (df["UserID"].isin(selected_users)) 
                    newdf_temp = df[filtrage]
                else:
                    filtrage= (df["UserID"].isin(selected_users) & df["TEMP"].astype(str).isin(selected_temps))
                    newdf_temp = df[filtrage]


            else : 
                if(selected_temps == []) :
                    newdf_temp = df
                else : 
                    filtrage= (df["TEMP"].astype(str).isin(selected_temps))
                    newdf_temp = df[filtrage]
            
        else : 
            selected_temps.append(checkbox_var_temp.get())
            print(selected_temps)
            if(selected_users != []):
                filtrage= (df["TEMP"].astype(str).isin(selected_temps) & df["UserID"].isin(selected_users))
            else:
                filtrage= (df["TEMP"].astype(str).isin(selected_temps))
            newdf_temp = df[filtrage]

        fillTable(newdf_temp, "Prout")

    workbook.save(filename= "test.xlsx")


    
    workbook3 = Workbook()

    for instance in stats: 
        ws = workbook3.create_sheet(title=str(instance.id))
        ws.append(["Time", "Activity"])
        donnees = instance.activity[:]
        for i, donnee in enumerate(donnees):
            heure = donnee[0]
            activite = donnee[1]
            ws.cell(row=i+1, column=1, value=heure)
            ws.cell(row=i+1, column=2, value=activite)
    workbook3.save("test_activite.xlsx")


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




    def fillTable(newdf, tab):
        
        df_list=list(newdf)
        df_rset=newdf.round(2).to_numpy().tolist()

        df_tree = ttk.Treeview(main_window.tabView.tab(tab), columns=df_list)
        for i in df_tree.get_children():
            df_tree.delete(i)
        df_tree["show"] = "headings"
        df_tree.grid(row=3, column=1, columnspan=3, padx=(20, 20), pady=(10, 10), sticky="ew")

        for i in df_list:
            df_tree.column(i,width=75,anchor='c')
            df_tree.heading(i,text=i)
        for dt in df_rset:
            v=[r for r in dt]
            df_tree.insert('','end', values=v)
    
    fillTable(df, "Prout")

    optionmenu1_var = customtkinter.StringVar(value=tri[0])
    optionmenu2_var = customtkinter.StringVar(value=triSE[0])

    optionmenu_user = customtkinter.CTkOptionMenu(master=main_window.tabView.tab("Prout"), dynamic_resizing=False, values = tri, command=optionmenu_triSFI_callback, variable=optionmenu1_var)
    optionmenu_user.grid(row=1, column=1, padx=(100, 100), pady=(20, 20), sticky="nsew")
    optionmenu_2 = customtkinter.CTkOptionMenu(master=main_window.tabView.tab("Prout"), dynamic_resizing=False, values = triSE, command=optionmenu_triSE_callback, variable=optionmenu2_var)
    optionmenu_2.grid(row=1, column=2,  padx=(100, 100), pady=(20, 20), sticky="nsew")
    optionmenu_3 = customtkinter.CTkOptionMenu(master=main_window.tabView.tab("Prout"), dynamic_resizing=False, values = users, command=optionmenu_triSFI_callback, variable=optionmenu1_var)
    optionmenu_3.grid(row=1, column=3,  padx=(100, 100), pady=(20, 20), sticky="nsew")
   
    zoom = 0.8


    img = Image.open("sfi_all_means.png")

    pixels_x, pixels_y = tuple([int(zoom * x)  for x in img.size])
    
    img = ImageTk.PhotoImage(img.resize((pixels_x, pixels_y)))
    panel = Label(main_window.tabView.tab("Tab 2"), image = img)
    panel.photo = img
    panel.grid(column=1, row=1, padx=(20, 20), pady=(10, 10), sticky="nsew")

    checkbox_var_users = customtkinter.StringVar(value=users[0])

    checkbox_frame = customtkinter.CTkScrollableFrame(main_window.tabView.tab("Prout"))
    checkbox_frame.grid(row=8, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
    checkbox_frame.grid_columnconfigure(1, weight=1)
    titre_checkbox = customtkinter.CTkLabel(master=checkbox_frame, text="Filtrer par user(s) : ", font=customtkinter.CTkFont(size=20))
    titre_checkbox.grid(row=1, column=1,  padx=(20, 20), pady=(10, 10), sticky="nsew")

    i = 1
    for user in users [1:] : 
        checkbox = customtkinter.CTkCheckBox(master=checkbox_frame, text=user, variable=checkbox_var_users, offvalue = user, onvalue = user, command=checkbox_user_callback)
        checkbox.grid(row=i +1, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        i = i+1
    

    def radiobuttonSelection():

        if(radio_var.get() == "Histogramme (moyennes)"):
            
            if(radio2_var.get() == "SFI"):
                img = Image.open("sfi_all_means.png")
            elif(radio2_var.get() == "Sleep efficiency (%)") : 
                img = Image.open("sleep_efficiency_all_means.png")
            elif(radio2_var.get() == "sleep_latency"): 
                img = Image.open("sleep_latency_all_means.png")
            elif(radio2_var.get() == "Tout"):
                img = Image.open("all_means.png")

            img = ImageTk.PhotoImage(img.resize((pixels_x, pixels_y)))
            panel = Label(main_window.tabView.tab("Tab 2"), image = img)
            panel.photo = img
            panel.grid(column=1, row=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        elif(radio_var.get() == "autre"): 
            img = Image.open("testPlot4.png")
            img = ImageTk.PhotoImage(img.resize((pixels_x, pixels_y)))
            panel = Label(main_window.tabView.tab("Tab 2"), image = img)
            panel.photo = img
            panel.grid(column=1, row=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        elif(radio_var.get() == "Boîtes à moustache"): 
            if(radio2_var.get() == "SFI"):
                img = Image.open("boxplotSFI.png")
            elif(radio2_var.get() == "Sleep efficiency (%)") : 
                    img = Image.open("boxplotSE.png")
            elif(radio2_var.get() == "sleep_latency"):
                    img = Image.open("boxplotSL.png")

            img = ImageTk.PhotoImage(img.resize((pixels_x, pixels_y)))
            panel = Label(main_window.tabView.tab("Tab 2"), image = img)
            panel.photo = img
            panel.grid(column=1, row=1, padx=(20, 20), pady=(10, 10), sticky="nsew")

    radiobutton_frame = customtkinter.CTkFrame(main_window.tabView.tab("Tab 2"))
    radiobutton_frame.grid(row=1, column=4, padx=(20, 20), pady=(10, 10), sticky="nsew")
    radio_var = tk.StringVar(value = "Histogramme (moyennes)")

    radiobutton1 = customtkinter.CTkRadioButton(master=radiobutton_frame, variable=radio_var, value = "Histogramme (moyennes)", text="Histogramme (moyennes)", command=radiobuttonSelection)
    radiobutton1.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="nsew")
    radiobutton2 = customtkinter.CTkRadioButton(master=radiobutton_frame, variable=radio_var, value = "autre", text="Cliquez ici si vous aimez Gaëlle", command=radiobuttonSelection)
    radiobutton2.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="nsew")
    radobutton3 = customtkinter.CTkRadioButton(master=radiobutton_frame, variable=radio_var, value = "Boîtes à moustache", text = "Boîtes à moustache", command=radiobuttonSelection)
    radobutton3.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")
    
    titre_radioframe = customtkinter.CTkLabel(master=radiobutton_frame, text="Type de graphe : ", font=customtkinter.CTkFont(size=20))
    titre_radioframe.grid(row=1, column=0,  padx=(20, 20), pady=(10, 10), sticky="nsew")


    checkbox_frame.grid_rowconfigure(2, weight=0)

    radiobutton_frame2 = customtkinter.CTkFrame(main_window.tabView.tab("Tab 2"))
    radiobutton_frame2.grid(row=3, column=4, padx=(20, 20), pady=(10, 10), sticky="nsew")
    radio2_var = tk.StringVar(value="SFI")
    radiobutton3 = customtkinter.CTkRadioButton(master=radiobutton_frame2, variable=radio2_var, value = "Sleep efficiency (%)", text="Sleep efficiency (%)", command=radiobuttonSelection)
    radiobutton3.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="nsew")
    radiobutton4 = customtkinter.CTkRadioButton(master=radiobutton_frame2, variable=radio2_var, value = "SFI", text="SFI", command=radiobuttonSelection)
    radiobutton4.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="nsew")
    radiobutton5 = customtkinter.CTkRadioButton(master=radiobutton_frame2, variable=radio2_var, value = "sleep_latency", text="sleep_latency", command=radiobuttonSelection)
    radiobutton5.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="nsew")
    radiobutton6 = customtkinter.CTkRadioButton(master=radiobutton_frame2, variable=radio2_var, value = "Tout", text="Tout", command=radiobuttonSelection)
    radiobutton6.grid(row=2, column=1, pady=(20, 0), padx=20, sticky="nsew")


    titre_radioframe2 = customtkinter.CTkLabel(master=radiobutton_frame2, text="Variable : ", font=customtkinter.CTkFont(size=20))
    titre_radioframe2.grid(row=1, column=0,  padx=(20, 20), pady=(10, 10), sticky="nsew")
    

    checkbox_var_temp = customtkinter.StringVar(value=temp[0])

    checkbox2_frame = customtkinter.CTkScrollableFrame(main_window.tabView.tab("Prout"))
    checkbox2_frame.grid(row=8, column=2, padx=(20, 20), pady=(10, 10), sticky="nsew")
    checkbox2_frame.grid_columnconfigure(1, weight=1)

    titre_checkbox2 = customtkinter.CTkLabel(master=checkbox2_frame, text="Filtrer par température : ", font=customtkinter.CTkFont(size=20))
    titre_checkbox2.grid(row=1, column=1,  padx=(20, 20), pady=(10, 10), sticky="nsew")

    i = 1
    for temperature in temp[1:] : 
        checkbox = customtkinter.CTkCheckBox(master=checkbox2_frame, text=temperature, variable=checkbox_var_temp, offvalue = temperature, onvalue = temperature, command=checkbox_temp_callback)
        checkbox.grid(row=i +1, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        i = i+1
    
    statsvar = customtkinter.StringVar(value=moy)
    fillTable(moydf, "Tab 2")



    


    
    


    

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