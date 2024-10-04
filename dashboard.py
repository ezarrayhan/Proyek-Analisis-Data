import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
hour = pd.read_csv('hour.csv')
hour['dteday'] = pd.to_datetime(hour['dteday'])

# Set mappings
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
year_map = {0: '2011', 1: '2012'}
month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
hour_map = {i: str(i + 1) for i in range(24)}
holiday_map = {0: 'Not Holiday', 1: 'Holiday'}
weekday_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
workingday_map = {0: 'Weekend or Holiday', 1: 'Working Day'}
weathersit_map = {
    1: 'Clear/ Few Clouds/ Partly Cloudy',
    2: 'Misty',
    3: 'Light Snow/ Light Rain/ Scattered Clouds',
    4: 'Heavy Rain/ Ice Pallets/ Snow + Fog'
}

# Replacing categorical value
hour['season'] = hour['season'].replace(season_map)
hour['yr'] = hour['yr'].replace(year_map)
hour['mnth'] = hour['mnth'].replace(month_map)
hour['hr'] = hour['hr'].replace(hour_map)
hour['holiday'] = hour['holiday'].replace(holiday_map)
hour['weekday'] = hour['weekday'].replace(weekday_map)
hour['workingday'] = hour['workingday'].replace(workingday_map)
hour['weathersit'] = hour['weathersit'].replace(weathersit_map)

# Drop unused columns
hour.drop(columns=['instant'], inplace=True)

# Define function for categorical analysis
def categorical_stats(hour, column):
    freq = hour.groupby(column)['cnt'].sum()
    prop = (freq / hour['cnt'].sum()) * 100
    min_values = hour.groupby(column)['cnt'].min()
    max_values = hour.groupby(column)['cnt'].max()
    mean_values = hour.groupby(column)['cnt'].mean()
    
    result = pd.DataFrame({
        'Frequency': freq,
        'Proportion (%)': prop.round(2),
        'Min': min_values,
        'Max': max_values,
        'Mean': mean_values.round(2)
    }).sort_values(by='Frequency', ascending=False)
    
    return result

# Start Streamlit App
st.title("Bike Sharing Dashboard")

# Tabs for different visualizations
tabs = st.tabs(["Overview", "Time Trend", "Seasonal Analysis", "Day & Holiday Analysis", "Weather Analysis"])

# --- Tab 1: Overview ---
with tabs[0]:
    st.header("Overview of Bike Sharing Data")
    st.write("Summary statistics for numerical variables:")
    st.dataframe(hour.describe())

    # Display stats for categorical variables
    st.write("Bike Sharing by Season:")
    result_season = categorical_stats(hour, 'season')
    st.dataframe(result_season)

# --- Tab 2: Time Trend ---
with tabs[1]:
    st.header("Bike Sharing Trend Over Time")

    daily_counts = hour.groupby('dteday')['cnt'].sum()

    # Plotting trend over time
    plt.figure(figsize=(12, 6))
    plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Total Count')
    plt.title('Trend of Bike Sharing Over Time')
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

# --- Tab 3: Seasonal Analysis ---
with tabs[2]:
    st.header("Bike Sharing by Season and Month")

    # Bar plot by season
    plt.figure(figsize=(15, 10))
    sns.barplot(x="season", y="cnt", data=hour, hue="season")
    plt.title("Number of Bike Sharing by Season")
    st.pyplot(plt)

    # Bar plot by month
    plt.figure(figsize=(15, 10))
    sns.barplot(x="mnth", y="cnt", data=hour, hue="mnth")
    plt.title("Number of Bike Sharing by Month")
    st.pyplot(plt)

# --- Tab 4: Day & Holiday Analysis ---
with tabs[3]:
    st.header("Analysis by Day and Holiday")

    # Bar plot by weekday
    plt.figure(figsize=(15, 10))
    sns.barplot(x="weekday", y="cnt", data=hour, hue="weekday")
    plt.title("Number of Bike Sharing by Days")
    st.pyplot(plt)

    # Pie chart for holiday
    plt.figure(figsize=(7, 7))
    holiday_counts = hour['holiday'].value_counts()
    plt.pie(holiday_counts, labels=holiday_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Number of Bike Sharing by Holiday')
    st.pyplot(plt)

# --- Tab 5: Weather Analysis ---
with tabs[4]:
    st.header("Analysis by Weather Conditions")

    # Pie chart for weather situations
    plt.figure(figsize=(7, 7))
    weather_counts = hour['weathersit'].value_counts()
    plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Number of Bike Sharing by Weather Situation')
    st.pyplot(plt)
