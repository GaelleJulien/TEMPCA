import pandas as pd
import matplotlib.pyplot as plt
import datetime as dte



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



# df2 = pd.read_excel("donnees_actimetres.xlsx", "05JB_32", skiprows=18)
# df2_columns = ["Time", "Activity"]

# df3 = df2[df2_columns]
# df3["Time"] = (df3["Time"]).astype(str)
# df3["Activity"] = df3["Activity"].astype(int)

# df3.set_index("Time")
# x_axis = df2["Time"].values
# fig = df3.plot(x="Time", y = "Activity").get_figure()
# fig.savefig("testPlot2.png")



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


