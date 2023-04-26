import pandas as pd


df = pd.DataFrame(pd.read_excel("test.xlsx"))

#filter = df["UserID"] == "08CN"

users = df["UserID"].drop_duplicates().to_list()

moy = df.groupby("temperature")[["sleep_efficiency (%)", "actual_sleep (%)", "actual_wake (%)", "fragmentation_index"]].mean()
moy = str(moy)
print(moy)