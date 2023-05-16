import pandas as pd
import matplotlib.pyplot as plt
import datetime as dte
import numpy as np
import re


#SLEEP FOUNDATION


optionsTri = ["SFI ordre croissant", "SFI ordre décroissant"]

optionsTriSE = ["Sleep efficiency ordre croissant", "Sleep efficiency ordre décroissant"]

df = pd.DataFrame(pd.read_excel("test.xlsx"))
# dfActivity = pd.DataFrame(pd.read_excel("test_activite.xlsx", sheet_name=None, index_col=0))
# print(dfActivity)

SFI_EC_total = df["SFI"].std()
SE_EC_total = df["sleep_efficiency (%)"].std()
AS_EC_total = df["actual_sleep (%)"].std()


dfsorted = df.sort_values(by = "SFI")

df_num = df.select_dtypes(include=["float"]).columns

users = ["Sujets..."]
df = df.astype({"TEMP" : str})
df["sleep_latency" ]= df["sleep_latency"].astype("string")

df["sleep_latency" ] = pd.to_timedelta(df["sleep_latency" ])



users.extend(df["UserID"].drop_duplicates().to_list())

temp = ["Température..."]
temp.extend(df["TEMP"].drop_duplicates().to_list())



tri = ["Trier en fonction du SFI..."]

tri.extend(optionsTri)

triSE = ["Trier en fonction de sleep_efficiency..."]
triSE.extend(optionsTriSE)

moydf = df

moydf = moydf.groupby("TEMP")[["sleep_efficiency (%)", "actual_sleep (%)", "actual_wake (%)", "sleep_latency", "SFI"]].mean()


fig, ax = plt.subplots()

moydf.reset_index(inplace = True)
moydf = moydf.rename(columns={"index" : "temperature"})
moydf["sleep_latency"] = moydf["sleep_latency"].astype(str).map(lambda x: x[7:15])

plotMoy = moydf.plot.bar(x = "TEMP")
plt.savefig("plotMoyennes.png")

#print(moydf["sleep_latency"])

moy = str(moydf)
moydf["sleep_latency"] =  pd.to_timedelta(moydf["sleep_latency" ])


def plotHypnnogramme(temperature):
    df2 = pd.read_excel("CombinedActivity.xlsx")

    
    df2['Time'] = pd.to_datetime(df2['Time'],  format="%H:%M:%S")
    
    
    df3 = df2.resample('H', on="Time").mean()
    df3.index = pd.to_datetime(df3.index)

    df3['DateTime'] = df3.index


    # Définir la plage horaire souhaitée
    start_time = pd.to_datetime('22:00:00').time()
    end_time = pd.to_datetime('07:00:00').time()

# Créer une fonction de tri personnalisée
    def custom_sort(time):
        if time.time() >= start_time:
            return time
        else:
            return time + pd.DateOffset(days=1)
    
    df3["Sorted"] = df3['DateTime'].map(custom_sort)
    df_sorted = df3.sort_values(by="Sorted")
    df_sorted = df_sorted.dropna()

    df_sorted.reset_index(drop=True)

    df_sorted.set_index("Sorted")

    # colonnesTout = []

    # for tempColonne in temp : 
    #         print(tempColonne)
    #         colonnesTout.append(df_sorted.filter(like = ("_" + tempColonne)).columns.to_list())
    # print(colonnesTout)
                

    colonnes = df_sorted.filter(like = temperature).columns.to_list()
    colonnesTout = df_sorted.filter(like = "_" ).columns.to_list()
    meanActivity = df_sorted[colonnes].mean(axis=1)
    meanActivityAll = df_sorted[colonnesTout].mean(axis=1)
    df_sorted["mean"] = meanActivity
    df_sorted["meanAll"] = meanActivityAll

    df_sorted.reset_index(drop=False)
    df_sorted["Sorted"] = df_sorted["Sorted"].dt.strftime("%H:%M:%S")

    # fig = df2.plot(x = "Time", y = "mean", legend=False).get_figure()
    # fig.savefig("testPlot2.png")
    # fig = df2.plot(x="Time", y = "mean").get_figure()
    # fig.savefig("testPlot2.png")

    figMean = df_sorted.plot.bar(x = "Sorted", y = "mean", rot = 1, ylim=(0,30), ylabel = "Activité", label = "température : " + temperature).get_figure()
    plt.locator_params(axis='x', nbins=7)
    plt.savefig("testMeanActivity.png")

    toutMean = df_sorted.plot.bar(x = "Sorted", y = "meanAll", rot = 1, ylim=(0,30), ylabel = "Activité", label = "température : " +temperature).get_figure()
    plt.locator_params(axis='x', nbins=7)
    plt.savefig("testAllMeanActivity.png")





dfBoxSE = pd.DataFrame(df[["sleep_efficiency (%)", "TEMP"]])
boxfig = dfBoxSE.plot.box(by="TEMP")
plt.savefig("boxplotSE.png")


dfBoxTimeSFI = pd.DataFrame(df[["SFI", "TEMP"]])
boxfig = dfBoxTimeSFI.plot.box(by="TEMP")
plt.savefig("boxplotSFI.png")


df["sleep_latency" ] = df["sleep_latency" ] / pd.Timedelta(minutes=1)
#print(df["sleep_latency"])
dfBoxTimeSL = pd.DataFrame(df[["sleep_latency", "TEMP"]])
boxfig = dfBoxTimeSL.plot.box(by="TEMP")
plt.savefig("boxplotSL.png")

df = pd.DataFrame(moydf[["sleep_efficiency (%)", "TEMP"]])
fig2 = df.plot.bar(x = "TEMP", y = "sleep_efficiency (%)", rot = 0,)
plt.savefig("sleep_efficiency_all_means.png")

df = pd.DataFrame(moydf[["SFI", "TEMP"]])
fig2 = df.plot.bar(x = "TEMP", y = "SFI", rot = 0)
plt.savefig("sfi_all_means.png")

moydf["sleep_latency" ] = moydf["sleep_latency" ] / pd.Timedelta(minutes=1)
df = pd.DataFrame(moydf[["sleep_latency", "TEMP"]])
fig3 = df.plot.bar(x = "TEMP", y = "sleep_latency", rot = 0,)
plt.savefig("sleep_latency_all_means.png")

df = pd.DataFrame(moydf)
fig3 = df.plot.bar(x = "TEMP", rot = 0,)
plt.savefig("all_means.png")

plotHypnnogramme("_32")

