import pandas as pd


df = pd.DataFrame(pd.read_excel("test.xlsx"))
filter = df["temperature"] == 16
print(df[filter])