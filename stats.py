import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

optionsTri = ["Ordre croissant (SFI)", "Ordre décroissant (SFI)"]

df = pd.DataFrame(pd.read_excel("test.xlsx"))

dfsorted = df.sort_values(by = "SFI")

df_num = df.select_dtypes(include=["float"]).columns

users = ["Trier par...."]
df = df.astype({"TEMP" : str})
users.extend(optionsTri)

temp = ["Température..."]
temp.extend(df["TEMP"].drop_duplicates().to_list())

moydf = df.groupby("TEMP")[["sleep_efficiency (%)", "actual_sleep (%)", "actual_wake (%)", "SFI"]].mean()
moy = str(moydf)

df2 = pd.read_excel("donnees_actimetres.xlsx", "05JB_32", skiprows=18)
df2_columns = ["Time", "Activity"]

df3 = df2[df2_columns]
df3["Time"] = (df3["Time"]).astype(str)
df3["Activity"] = df3["Activity"].astype(int)

df3.set_index("Time")
print (df3["Time"])
x_axis = df2["Time"].values
fig = df3.plot(x="Time", y = "Activity").get_figure()
fig.savefig("testPlot2.png")

df = pd.DataFrame(moydf["sleep_efficiency (%)"])
fig2 = df.plot(kind="bar", grid=True)
fig2.get_figure().savefig("sleep_efficiency_all_means.png")


df = pd.DataFrame(moydf["SFI"])
fig2 = df.plot(kind="bar", grid=True)
fig2.get_figure().savefig("sfi_all_means.png")



# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# ax = df.plot.bar(x='lab', y='val', rot=0)
# ax.get_figure().savefig("testPlot3")
