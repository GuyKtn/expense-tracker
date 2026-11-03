import pandas as pd

df = pd.read_csv("sample_data/expenses_sample.csv", parse_dates=["day"])

print(df.head())      # first 5 rows
print(df.shape)       # (rows, columns)
print(df.dtypes)      # type of each column
print(df.describe())  # statistics for numeric columns

print(df.groupby("category")["amount"].sum().sort_values(ascending=False))  # total amount per category
print(df.groupby("category")["amount"].mean().sort_values(ascending=False))  # average amount per category

df["month"] = df["day"].dt.to_period("M")
monthly_totals = df.groupby("month")["amount"].sum()
print(monthly_totals)  # total amount per month

print(df.nlargest(1, "amount"))  # largest expense