import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import re




optionsTri = ["SFI ordre croissant", "SFI ordre décroissant"]

optionsTriSE = ["Sleep efficiency ordre croissant", "Sleep efficiency ordre décroissant"]

dfTest = pd.DataFrame(pd.read_excel("test.xlsx"))
df_hour = pd.DataFrame(pd.read_excel("activityData.xlsx"))
# dfActivity = pd.DataFrame(pd.read_excel("test_activite.xlsx", sheet_name=None, index_col=0))
# print(dfActivity)

SFI_EC_total = dfTest["SFI"].std()
SE_EC_total = dfTest["sleep_efficiency (%)"].std()
AS_EC_total = dfTest["actual_sleep (%)"].std()


df_num = dfTest.select_dtypes(include=["float"]).columns

users = ["Sujets..."]
dfTest = dfTest.astype({"NUIT" : str})
dfTest["sleep_latency" ]= dfTest["sleep_latency"].astype("string")
dfTest["TST" ]= dfTest["TST"].astype("string")
dfTest["TIB" ]= dfTest["TIB"].astype("string")
dfTest["SPT" ]= dfTest["SPT"].astype("string")
dfTest["actual_wake_time" ]= dfTest["actual_wake_time"].astype("string")



dfTest["sleep_latency" ] = pd.to_timedelta(dfTest["sleep_latency" ])
dfTest["TST" ] = pd.to_timedelta(dfTest["TST" ])
dfTest["TIB" ] = pd.to_timedelta(dfTest["TIB" ])
dfTest["SPT" ] = pd.to_timedelta(dfTest["SPT" ])
dfTest["actual_wake_time" ] = pd.to_timedelta(dfTest["actual_wake_time" ])




# Liste des colonnes à traiter
colonnes_a_traiter = [colonne for colonne in dfTest.columns if dfTest[colonne].dtype != object]  # Exclure les colonnes de type 'object' (chaînes de caractères)

resultats = {}

groupes = dfTest.groupby('NUIT')

for groupe, data_grouped in groupes:
    resultats[groupe] = {}
    for colonne in colonnes_a_traiter:
        if pd.api.types.is_timedelta64_dtype(data_grouped[colonne].dtype):
            mediane = data_grouped[colonne].mean()
            ecart_type = data_grouped[colonne].std()
            resultats[groupe][colonne] = f"{mediane} ± {ecart_type}"
        else:
            mediane = round(data_grouped[colonne].mean(), 2)
            ecart_type = round(data_grouped[colonne].std(), 2)
            resultats[groupe][colonne] = f"{mediane} ± {ecart_type}"



df_hour["mean_sleep_bouts" ]= df_hour["mean_sleep_bouts"].astype("string")
df_hour["mean_wake_bouts" ]= df_hour["mean_wake_bouts"].astype("string")

df_hour["mean_sleep_bouts" ] = pd.to_timedelta(df_hour["mean_sleep_bouts" ])
df_hour["mean_wake_bouts" ] = pd.to_timedelta(df_hour["mean_wake_bouts" ])


# Liste des colonnes à traiter
colonnes_a_traiter = [colonne for colonne in df_hour.columns if df_hour[colonne].dtype != object]  # Exclure les colonnes de type 'object' (chaînes de caractères)

resultats = {}

groupes = df_hour.groupby('NUIT')

for groupe, data_grouped in groupes:
    resultats[groupe] = {}
    for colonne in colonnes_a_traiter:
        if pd.api.types.is_timedelta64_dtype(data_grouped[colonne].dtype):
            mediane = data_grouped[colonne].mean()
            ecart_type = data_grouped[colonne].std()
            resultats[groupe][colonne] = f"{mediane} ± {ecart_type}"
        else:
            mediane = round(data_grouped[colonne].mean(), 2)
            ecart_type = round(data_grouped[colonne].std(), 2)
            resultats[groupe][colonne] = f"{mediane} ± {ecart_type}"


df_hour["mean_immobile_bouts"] = df_hour["mean_immobile_bouts"].astype("string")
df_hour["mean_immobile_bouts"] = pd.to_timedelta(df_hour["mean_immobile_bouts"])

tri = ["Trier en fonction du SFI..."]

tri.extend(optionsTri)

triSE = ["Trier en fonction de sleep_efficiency..."]
triSE.extend(optionsTriSE)

moydf = dfTest

moydf = moydf.groupby("NUIT")[["sleep_efficiency (%)", "TST","actual_sleep (%)", "actual_wake (%)", "sleep_latency", "SFI"]].mean()
moydfHour = df_hour.groupby("NUIT")[["sleep_bouts", "wake_bouts", "mean_immobile_bouts"]].mean()
moydfHour.reset_index(inplace=True)
moydfHour["mean_immobile_bouts"] = moydfHour["mean_immobile_bouts"].astype(str)


fig, ax = plt.subplots()

moydf.reset_index(inplace = True)
moydf = moydf.rename(columns={"index" : "nuit"})
moydf["sleep_latency"] = moydf["sleep_latency"].astype(str).map(lambda x: x[7:15])
moydf["TST"] = moydf["TST"].astype(str).map(lambda x: x[7:15])


plotMoy = moydf.plot.bar(x = "NUIT", xlabel = "Nuit", ylabel = "????")
plt.savefig("plotMoyennes.png")


moy = str(moydf)
moydf["sleep_latency"] =  pd.to_timedelta(moydf["sleep_latency" ])


df2 = pd.read_excel("CombinedActivity.xlsx")

    
df2['Time'] = pd.to_datetime(df2['Time'],  format="%H:%M:%S")
    
def taux_sup_20(x):
    return (x > 20).mean()

df2.set_index("Time", inplace=True)
df3 = df2.groupby(pd.Grouper(freq="30Min")).apply(lambda x: (x > 20).mean() * 100)

#df3 = df2.resample('15Min', on="Time").mean()
df3.index = pd.to_datetime(df3.index)

df3['DateTime'] = df3.index

    # Définir la plage horaire souhaitée
start_time = pd.to_datetime('22:00:00').time()
end_time = pd.to_datetime('07:00:00').time()

def custom_sort(time):
    if time.time() >= start_time:
        return time
    else:
        return time + pd.DateOffset(days=1)
    
df3["Heure"] = df3['DateTime'].map(custom_sort)
df_sorted = df3.sort_values(by="Heure")
df_sorted = df_sorted.dropna()

df_sorted.reset_index(drop=True)

df_sorted.set_index("Heure")

df_sorted['Heure'] = pd.to_datetime(df_sorted['Heure'], format='%H:%M:%S')

df_sorted["Hour"] = (df_sorted["Heure"].dt.hour)

newcolumns = ["Heure"] + [col for col in df_sorted.columns if col !="Heure" ]
df_sorted = df_sorted[newcolumns]



def taux_sup_20(column):
    count_sup_20 = sum(column > 20)  
    total_count = len(column)  
    taux = count_sup_20 / total_count  
    return taux


df_hourly = df_sorted.groupby("Hour", sort=False).mean()
df_hourly = df_hourly.drop(columns=["DateTime", "Heure"])

    
# Calculer le taux d'éveil pour chaque heure
df_hourly['AwakeningRate'] = (df_hourly.iloc[:, 1:] >= 20).mean(axis=1) * 100  # Assuming columns from 1 represent users
print(df_hourly)

fig, ax = plt.subplots()
ax.bar(df_hourly.index, df_hourly['AwakeningRate'])

ax.set_xlabel('Heure')
ax.set_ylabel("Taux d'éveil (%)")
ax.set_title("Taux d'éveil par heure")
plt.savefig("Wakefulness_Rate_per_Hour.png")


def plotHypnnogramme(temperature):

    colonnes = df_sorted.filter(like = temperature).columns.to_list()
    colonnesTout = df_sorted.filter(like = "_" ).columns.to_list()
    df_sorted['Heure'] = pd.to_datetime(df_sorted['Heure'], format='%H:%M:%S')

    meanActivity = df_sorted[colonnes].mean(axis=1)
    meanActivityAll = df_sorted[colonnesTout].mean(axis=1)
    df_sorted["mean"] = meanActivity
    df_sorted["meanAll"] = meanActivityAll

    df_sorted.reset_index(drop=False)
    df_sorted["Heure"] = df_sorted["Heure"].dt.strftime("%H:%M:%S")

    figMean = df_sorted.plot.bar(x = "Heure", y = "mean", rot = 1, ylim=(0,30),xlabel = "Heure", ylabel = "Activité", label = "Nuit: " + temperature).get_figure()
    plt.locator_params(axis='x', nbins=7)
    plt.savefig("testMeanActivity.png")



def plotHourbyUser(user, temperature) : 
    if(temperature == "Tout") : 
        colonnes = df_sorted.filter(like = user).columns.to_list()
        colonnesTout = df_sorted.filter(like = "_" ).columns.to_list()
        
    else: 
        colonnes = df_sorted.filter(like = user).filter(like=temperature).columns.to_list()
        colonnesTout = df_sorted.filter(like=temperature).columns.to_list()
    print (colonnes)
    df_sorted['Heure'] = pd.to_datetime(df_sorted['Heure'], format='%H:%M:%S')

    meanActivity = df_sorted[colonnes].mean(axis=1)
    df_sorted["mean"] = meanActivity
    meanActivityAll = df_sorted[colonnesTout].mean(axis=1)


    df_sorted["meanAll"] = meanActivityAll



    df_sorted.reset_index(drop=False)
    df_sorted["Heure"] = df_sorted["Heure"].dt.strftime("%H:%M:%S")

    figUser = df_sorted.plot(x = "Heure", y = "meanAll", rot = 1, ylim=(0,50), xlabel = "Heure", ylabel = "Activité", label= "Moy tous les sujets", color = "red")
    
    if(temperature == "Tout") : 
        figUser2 = df_sorted.plot.bar(x = "Heure", y = "meanAll", rot = 1, ylim=(0,50), xlabel = "Heure", ylabel = "Activité", ax = figUser).get_figure()
    else :    
        figUser2 = df_sorted.plot.bar(x = "Heure", y = "mean", rot = 1, ylim=(0,50), xlabel = "Heure", ylabel = "Activité", label= user + " " + temperature, ax = figUser).get_figure()

    plt.locator_params(axis='x', nbins=7)
    plt.savefig("userHour.png")

dfBoxSE = pd.DataFrame(dfTest[["sleep_efficiency (%)", "NUIT"]])
boxfig = dfBoxSE.plot.box(by="NUIT", xlabel = "Nuit", ylabel = "Sleep efficiency (%)")
plt.savefig("boxplotSE.png")


dfBoxTimeSFI = pd.DataFrame(dfTest[["SFI", "NUIT"]])
boxfig = dfBoxTimeSFI.plot.box(by="NUIT", xlabel = "Nuit", ylabel = "Sleep Fragmentation Index")
plt.savefig("boxplotSFI.png")


dfTest["sleep_latency" ] = dfTest["sleep_latency" ] / pd.Timedelta(minutes=1)
dfBoxTimeSL = pd.DataFrame(dfTest[["sleep_latency", "NUIT"]])
boxfig = dfBoxTimeSL.plot.box(by="NUIT", xlabel = "Nuit", ylabel = "Sleep Latency (minutes)")
plt.savefig("boxplotSL.png")

dfTest = pd.DataFrame(moydf[["sleep_efficiency (%)", "NUIT"]])
fig2 = dfTest.plot.bar(x = "NUIT", y = "sleep_efficiency (%)", rot = 0, xlabel = "Nuit", ylabel = "Sleep efficiency (%)")
plt.savefig("sleep_efficiency_all_means.png")

dfTest = pd.DataFrame(moydf[["SFI", "NUIT"]])
fig2 = dfTest.plot.bar(x = "NUIT", y = "SFI", rot = 0, xlabel = "Nuit", ylabel = "Sleep Fragmentation Index")
plt.savefig("sfi_all_means.png")

moydf["sleep_latency" ] = moydf["sleep_latency" ] / pd.Timedelta(minutes=1)
dfTest = pd.DataFrame(moydf[["sleep_latency", "NUIT"]])
fig3 = dfTest.plot.bar(x = "NUIT", y = "sleep_latency", rot = 0, xlabel = "Nuit", ylabel = "Sleep Latency (minutes)")
plt.savefig("sleep_latency_all_means.png")

dfTest = pd.DataFrame(moydf)
fig3 = dfTest.plot.bar(x = "NUIT", rot = 0)
plt.savefig("all_means.png")

plotHypnnogramme("_32")

