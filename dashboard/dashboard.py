import streamlit as st # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import seaborn as sns

st.title("Bike Sharing (2011 - 2012)")
st.write("#### _MC004D5Y1124 - Rasendra Akbar Satyatama_")
st.write("source: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data")
st.write("----------------------------------------------------------------------------------\n")

days_df = pd.read_csv('main_data.csv)

with st.sidebar:
    option = option_menu("Dashboard", ['Time Series', 'Factors'], default_index=0)
    
if(option == 'Time Series'):
    col1, col2, col3 = st.columns(3)
    total_count = days_df['count'].sum()
    avg_per_day = days_df['count'].mean()
    std_dev = days_df['count'].std()
    col1.metric(label="Total Count", value=f"{total_count:,.0f}")
    col2.metric(label="Average per Day", value=f"{round(avg_per_day,2)}")
    col3.metric(label="Standar Deviation", value=f"{round(std_dev,2)}")
    
    st.write("#### Time Series Plot of Bike Sharing (2011 - 2012)")
    days_df['dteday'] = pd.to_datetime(days_df['dteday'])

    min_date = days_df['dteday'].min().date()
    max_date = days_df['dteday'].max().date()

    start_date, end_date = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = days_df[(days_df['dteday'] >= start_date) & (days_df['dteday'] <= end_date)]
    st.line_chart(filtered_df.set_index('dteday')['count'])
    
    st.write("#### Count Distribution")
    plt.style.use("dark_background")
    bins = st.slider("Select Number of Bins", min_value=5, max_value=50, value=20)

    fig, ax = plt.subplots()
    sns.histplot(days_df['count'], bins=bins, kde=True, color="#00BFFF", edgecolor="white", alpha=0.8)

    ax.set_title("Distribution of Bike Rentals", color="white")
    ax.set_xlabel("Count", color="white")
    ax.set_ylabel("Frequency", color="white")

    st.pyplot(fig)
    
if option == "Factors":
    category_option = st.selectbox("Select Category", ["Weekday", "Month", "Year"])

    category_mapping = {
        "Weekday": "weekday",
        "Month": "month",
        "Year": "year"
    }
    
    selected_category = category_mapping[category_option]

    st.write(f"#### Total Bike Rentals by {category_option}")
    
    grouped_df = days_df.groupby(selected_category)['count'].sum().reset_index()

    st.bar_chart(data=grouped_df, x=selected_category, y="count", use_container_width=True)

    factor_option = st.selectbox("Select Factor", ["Season", "Weather"])

    if factor_option == "Season":
        st.write("#### Total Bike Rentals by Season")
        season_df = days_df.groupby("season")["count"].sum().reset_index()
        st.bar_chart(data=season_df, x="season", y="count", use_container_width=True)
    
    elif factor_option == "Weather":
        st.write("#### Total Bike Rentals by Weather")
        weather_df = days_df.groupby("weather")["count"].sum().reset_index()
        st.bar_chart(data=weather_df, x="weather", y="count", use_container_width=True)
    
    st.write("#### Correlation Heatmap for Numerical Variables")
    excluded_columns = ["instant", "year", "month", "holiday", "weekday", "workingday", "season", "weather"]
    numeric_cols = [col for col in days_df.select_dtypes(include=["float64", "int64"]).columns if col not in excluded_columns]

    corr_matrix = days_df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig)
