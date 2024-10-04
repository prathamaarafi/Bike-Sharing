import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.header('Bike Dashboard')

df = pd.read_csv('Dashboard/all_data.csv')

df['dteday'] = pd.to_datetime(df['dteday'])

df['year'] = df['dteday'].dt.year
df['month'] = df['dteday'].dt.month

with st.sidebar:
    years = df['year'].unique()
    selected_year = st.selectbox('Select Year', years, index=0)
    
    months = df[df['year'] == selected_year]['month'].unique()
    selected_month = st.selectbox('Select Month', months, index=0)

if selected_year and selected_month:
    filtered_df = df[(df['year'] == selected_year) & (df['month'] == selected_month)]

    filtered_df['is_weekday'] = np.where(filtered_df['holiday'] == 1, 'holiday', 'weekday')

    avg_visitors_weekday = filtered_df.groupby('is_weekday')['cnt'].mean().reset_index()

    avg_visitors_hum = filtered_df.groupby('hum')['cnt'].mean().reset_index()

    
    st.subheader(f'Average Visitors: Weekday vs Holiday for {selected_month}/{selected_year}')
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(avg_visitors_weekday['is_weekday'], avg_visitors_weekday['cnt'], color=['skyblue', 'salmon'])
    ax1.set_title(f'Average Visitors: Weekday vs Holiday in {selected_month}/{selected_year}')
    ax1.set_xlabel('Day Type')
    ax1.set_ylabel('Average Visitor Count')
    st.pyplot(fig1)

    st.subheader(f'Average Visitors by Humidity Level for {selected_month}/{selected_year}')
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(avg_visitors_hum['hum'], avg_visitors_hum['cnt'], marker='o', color='skyblue')
    ax2.set_title(f'Average Visitors by Humidity Level in {selected_month}/{selected_year}')
    ax2.set_xlabel('Humidity')
    ax2.set_ylabel('Average Visitor Count')
    st.pyplot(fig2)
