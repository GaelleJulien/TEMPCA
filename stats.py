import pandas as pd




df = pd.DataFrame(pd.read_excel("test.xlsx"))

dfsorted = df.sort_values(by = "SFI")

df_num = df.select_dtypes(include=["float"]).columns

#filter = df["UserID"] == "05JB"
users = ["Sujets..."]
df = df.astype({"TEMP" : str})
users.extend(df["UserID"].drop_duplicates().to_list())
print (users)

temp = ["Température..."]
temp.extend(df["TEMP"].drop_duplicates().to_list())

moydf = df.groupby("TEMP")[["sleep_efficiency (%)", "actual_sleep (%)", "actual_wake (%)", "SFI"]].mean()
moy = str(moydf)
