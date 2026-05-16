# Python Project 3: Analyzing NYPD Arrests Data (Historic)

# Step 1: load all the necessary libraries for the project and read the data file. 
# We will use pandas and numpy for descriptive statistics and data cleaning.
# We will use matplotlib and seaborn for visualization.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("NYPD_Arrests_Data_(Historic)_20260515.csv")

# Step 2: Understanding the data and the column types. 

print(df.info())
print(df.describe())

# This dataset contains 19 columns: floats, integers, and strings. 

# Looking at the most frequently arrested age group, the offence and the precinct with the most arrests.

print(df['AGE_GROUP'].mode())
print(df['LAW_CAT_CD'].mode())
print(df['ARREST_PRECINCT'].mode())

# Step 3: Data Cleaning
# Since it's a large dataset, I want to narrow it down to focus on a specific timeframe. 

# Converting string column to datetime

df["ARREST_DATE"] = pd.to_datetime(
    df["ARREST_DATE"],
    format="%m/%d/%Y"
)

# Our research will focus on all arrests made in 2024 and 2025.

my_data = df[
    df["ARREST_DATE"].dt.year.isin([2024, 2025])
]

# Difference in entries between the original and filtered datasets. 

print(len(df))
print(len(my_data))

print(my_data)

# 6,264,978 entries vs 539,456 entries.

# Looking for any missing values in the new dataset and replacing them with "na" for strings or 0 for integers. 

print(my_data.isnull().sum())

my_data["PD_CD"] = my_data["PD_CD"].fillna("0")
my_data["KY_CD"] = my_data["KY_CD"].fillna("0")
my_data["LAW_CAT_CD"] = my_data["LAW_CAT_CD"].fillna("na")
my_data["Latitude"] = my_data["Latitude"].fillna("0")
my_data["Longitude"] = my_data["Longitude"].fillna("0")
my_data["Lon_Lat"] = my_data["Lon_Lat"].fillna("0")

print(my_data.isnull().sum())

# Now, keeping columns I need to answer the following questions - 
# 1. Did arrests year over year increase or decrease between 2024 and 2025 in each level of offence. 
# 2. Felony offense by borough over the years.

subset = my_data[['ARREST_KEY', 'ARREST_DATE', 'LAW_CAT_CD', 'ARREST_BORO']]

# Step 4: Data Analysis 

# Q1 Arrests by year + bar chart -  

print(
    subset["ARREST_DATE"]
    .dt.year
    .value_counts()
    .sort_index()
)

year_counts = (
    subset["ARREST_DATE"]
    .dt.year
    .value_counts()
    .sort_index()
)

year_counts.plot(kind="bar")

plt.title("Arrests by Year")
plt.xlabel("Year")
plt.ylabel("Number of Arrests")

plt.show()

# Q2, first we extract the year from the date, then extract only felonies from arrest category, 
# and finally, identify felony count by year and borough.

subset["YEAR"] = subset["ARREST_DATE"].dt.year

felonies = subset[
    subset["LAW_CAT_CD"] == "F"
]

felony_trend = (
    felonies
    .groupby(["YEAR", "ARREST_BORO"])
    .size()
    .reset_index(name="FELONY_ARRESTS")
)

print(felony_trend)

plt.figure(figsize=(12,6))

sns.barplot(
    data=felony_trend,
    x="YEAR",
    y="FELONY_ARRESTS",
    hue="ARREST_BORO"
)

plt.title("Felony Arrests by Borough Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Felony Arrests")

plt.show()

# Conclusion: We can see that overall arrests increased from 2024 to 2025. 
# Focusing on felony arrests by boroughs over the year, the bar chart doesn’t show any significant increase in arrests in each borough, 
# but we can see a slight increase on our data table. In both 2024 and 2025, Staten Island saw the least amount of felony arrests.
