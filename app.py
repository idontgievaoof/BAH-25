import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set up the app
st.set_page_config(page_title="Delhi Air Quality Grid", layout="wide")
st.title("Delhi Air Quality Grid: PM₂.₅ and PM₁₀ Heatmaps")

# Upload or load CSV data
df = pd.read_csv("delhi_air_quality_grid.csv")
df['time'] = pd.to_datetime(df['time'])

# Sidebar controls
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date", value=pd.to_datetime("2025-07-23"))
hour_range = st.sidebar.slider("Hour Range", min_value=0, max_value=23, value=(0, 6))
metric = st.sidebar.radio("Pollutant", ["pm25", "pm10"])

# Filter the data by date and hour
filtered_df = df[(df['time'].dt.date == selected_date) &
                 (df['time'].dt.hour >= hour_range[0]) &
                 (df['time'].dt.hour <= hour_range[1])]

if filtered_df.empty:
    st.warning("No data available for the selected date and time range.")
else:
    # Pivot the table to create a grid
    pivot = filtered_df.pivot_table(
        index='latitude', columns='longitude', values=metric, aggfunc='mean')

    # Sort for consistent heatmap orientation
    pivot = pivot.sort_index(ascending=False)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, ax=ax, cmap="inferno", cbar_kws={'label': f'{metric.upper()} concentration (μg/m³)'})
    ax.set_title(f"Heatmap of {metric.upper()} on {selected_date} ({hour_range[0]}:00 - {hour_range[1]}:00)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    st.pyplot(fig)
