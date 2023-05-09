import pandas as pd
import matplotlib.pyplot as plt
import datetime as dte



optionsTri = ["SFI ordre croissant", "SFI ordre décroissant"]

optionsTriSE = ["Sleep efficiency ordre croissant", "Sleep efficiency ordre décroissant"]

df = pd.DataFrame(pd.read_excel("test.xlsx"))


dfsorted = df.sort_values(by = "SFI")

df_num = df.select_dtypes(include=["float"]).columns

#filter = df["UserID"] == "05JB"
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



moydf.reset_index(inplace = True)
moydf = moydf.rename(columns={"index" : "temperature"})
moydf["sleep_latency"] = moydf["sleep_latency"].astype(str).map(lambda x: x[7:15])
print(moydf["sleep_latency"])

moy = str(moydf)



df2 = pd.read_excel("donnees_actimetres.xlsx", "05JB_32", skiprows=18)
df2_columns = ["Time", "Activity"]

df3 = df2[df2_columns]
df3["Time"] = (df3["Time"]).astype(str)
df3["Activity"] = df3["Activity"].astype(int)

df3.set_index("Time")
x_axis = df2["Time"].values
fig = df3.plot(x="Time", y = "Activity").get_figure()
fig.savefig("testPlot2.png")


dfBox = pd.DataFrame(df[["sleep_efficiency (%)", "TEMP"]])
boxfig = dfBox.plot.box(by="TEMP")
plt.savefig("boxplot2.png")

dfBoxTime = pd.DataFrame(df[["SFI", "TEMP"]])
boxfig = dfBoxTime.plot.box(by="TEMP")
plt.savefig("boxplot3.png")


df = pd.DataFrame(moydf["sleep_efficiency (%)"])
fig2 = df.plot(kind="bar", grid=True)
fig2.get_figure().savefig("sleep_efficiency_all_means.png")


df = pd.DataFrame(moydf["SFI"])
fig2 = df.plot(kind="bar", grid=True)
fig2.get_figure().savefig("sfi_all_means.png")

# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# ax = df.plot.bar(x='lab', y='val', rot=0)
# ax.get_figure().savefig("testPlot3")
