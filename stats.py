import pandas as pd




df = pd.DataFrame(pd.read_excel("test.xlsx"))

filter = df["UserID"] == "05JB"

users = df["UserID"].drop_duplicates().to_list()

moydf = df.groupby("temperature")[["sleep_efficiency (%)", "actual_sleep (%)", "actual_wake (%)", "fragmentation_index"]].mean()
moy = str(moydf)


print(moydf)
