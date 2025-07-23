import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# App config
st.set_page_config(page_title="Air Quality Map", layout="wide")
st.title("Air Quality Map: PM₂.₅ and PM₁₀ Heatmap")

# Load data
df = pd.read_csv("testing.csv")
df['time'] = pd.to_datetime(df['time'])

# Sidebar controls
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date", value=pd.to_datetime("2025-07-23"))
selected_hour = st.sidebar.slider("Select Hour", min_value=0, max_value=23, value=12)
metric = st.sidebar.radio("Pollutant", ["pm25", "pm10"])

# Filter data
filtered_df = df[(df['time'].dt.date == selected_date) &
                 (df['time'].dt.hour == selected_hour)]

if filtered_df.empty:
    st.warning("No data available for the selected date and hour.")
else:
    fig = px.density_heatmap(
        filtered_df,
        x="longitude",
        y="latitude",
        z=metric,
        color_continuous_scale="inferno",
        histfunc="avg",
        nbinsx=20,
        nbinsy=20,
        labels={metric: f"{metric.upper()} (μg/m³)"},
        hover_data={metric: True, "longitude": True, "latitude": True}
    )

    fig.update_layout(
        title=f"Heatmap of {metric.upper()} on {selected_date} at {selected_hour}:00",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)
