import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
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

    average_rentals = filtered_df.groupby('holiday')['cnt'].mean().reset_index()
    average_rentals.columns = ['Holiday', 'Average Rentals']

    average_rentals_hum = filtered_df.groupby('hum')['cnt'].mean().reset_index()

    st.subheader(f'Average Visitors: Weekday vs Holiday for {selected_month}/{selected_year}')
    plt.figure(figsize=(10, 6))
    sns.barplot(data=average_rentals, x='Holiday', y='Average Rentals', color='#FFB3BA', legend=False)
    plt.title(f'Perbandingan Rata-rata Pengunjung: Weekday vs Holiday di {selected_month}/{selected_year}')
    plt.ylabel('Rata-rata Pengunjung')
    plt.xlabel('Tipe Hari')
    plt.xticks(ticks=[0, 1], labels=['Weekday', 'Holiday'])
    plt.show()
    st.pyplot(plt.gcf())

    st.subheader(f'Average Visitors by Humidity Level for {selected_month}/{selected_year}')

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hum', y='cnt', data=average_rentals_hum, alpha=0.9, color='skyblue')
    plt.title(f'Pengaruh Kelembaban Terhadap Rata-rata Pengunjung di {selected_month}/{selected_year}')
    plt.xlabel('Kelembaban (%)')
    plt.ylabel('Rata-rata Pengunjung')
    plt.show()
    st.pyplot(plt.gcf())
