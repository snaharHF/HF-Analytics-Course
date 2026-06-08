# Python Project 2: Diabetes Data Analysis

import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/niteen11/DataAnalyticsAcademy/master/Python/dataset_diabetes/diabetic_data.csv"

df = pd.read_csv(url)

# Preview the data
print(df.head())

# This dataset uses "?" for missing values so I will replace "?" with "NA" for missing values.
# Since for my project, I want to compare different race groups, I will remove rows where race is missing.

df["race"] = df["race"].replace("?", pd.NA)

df = df.dropna(subset=["race"])

# For this project, I will compare the "Caucasian" and "AfricanAmerican" race groups time in hospital.

comparison = df[df["race"].isin(["Caucasian", "AfricanAmerican"])].copy()

stats = (
    comparison
    .groupby("race")["time_in_hospital"]
    .agg(["count", "mean", "median", "std", "min", "max"])
    .round(2)
)

print("Time in Hospital by Race Groups")
print(stats)

# We can see that on average, African American patients spend a slightly higher time in the hospital than Caucasian patients,
# event though the count of Caucasian patients is much higher than African American patients in the dataset.

avg_stay = (
    comparison
    .groupby("race")["time_in_hospital"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(7, 5))
avg_stay.plot(kind="bar")

plt.title("Average Time in Hospital by Race Group")
plt.xlabel("Race")
plt.ylabel("Average Time in Hospital (Days)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# Conclusion: African American patients had a slightly higher average 
# time in hospital than Caucasian patients. The difference is small, 
# so this should be interpreted as a descriptive observation only.