import pandas as pd




df = pd.DataFrame(pd.read_excel("test.xlsx"))

df_num = df.select_dtypes(include=["float"]).columns

filter = df["UserID"] == "05JB"

users = df["UserID"].drop_duplicates().to_list()

moydf = df.groupby("TEMP")[["sleep_efficiency (%)", "actual_sleep (%)", "actual_wake (%)", "SFI"]].mean()
moy = str(moydf)


