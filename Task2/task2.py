import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("C:\\Users\\abira\\OneDrive\\Desktop\\Unemployment in India.csv")


df.columns = df.columns.str.strip()


df = df.rename(columns={
    "Estimated Unemployment Rate (%)": "UnemploymentRate",
    "Estimated Employed": "Employed",
    "Estimated Labour Participation Rate (%)": "LPR"
})


df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")


df = df.dropna()

print("Basic Info:\n", df.info())
print("\nSummary Statistics:\n", df.describe())

region_avg = df.groupby("Region")["UnemploymentRate"].mean().sort_values(ascending=False)
print("\nAverage unemployment by region:\n", region_avg)


plt.figure(figsize=(12,6))
sns.lineplot(x="Date", y="UnemploymentRate", data=df, marker="o")
plt.axvline(pd.to_datetime("2020-03-01"), color="red", linestyle="--", label="Covid Start (Mar 2020)")
plt.title("Unemployment Rate in India (2019–2020)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.show()


pre_covid = df[df["Date"] < "2020-03-01"]["UnemploymentRate"].mean()
post_covid = df[df["Date"] >= "2020-03-01"]["UnemploymentRate"].mean()

print(f"\nAverage Unemployment Before Covid (till Feb 2020): {pre_covid:.2f}%")
print(f"Average Unemployment During Covid (Mar–Jun 2020): {post_covid:.2f}%")

plt.bar(["Pre-Covid", "During Covid"], [pre_covid, post_covid], color=["green", "red"])
plt.title("Covid-19 Impact on Unemployment")
plt.ylabel("Average Unemployment Rate (%)")
plt.show()


df["Month"] = df["Date"].dt.month
monthly_trend = df.groupby("Month")["UnemploymentRate"].mean()

plt.figure(figsize=(10,6))
monthly_trend.plot(kind="bar", color="skyblue")
plt.title("Seasonal Trend of Unemployment (Monthly Average)", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Average Unemployment Rate (%)")
plt.show()


top_regions = df.groupby("Region")["UnemploymentRate"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_regions.values, y=top_regions.index, palette="viridis")
plt.title("Top 10 Regions with Highest Average Unemployment", fontsize=14)
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("Region")
plt.show()