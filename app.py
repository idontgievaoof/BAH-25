import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime

# Set up the app
st.set_page_config(page_title="Air Quality Map", layout="wide")
st.title("Air Quality Map: PM₂.₅ and PM₁₀ Heatmaps")

# Upload or load CSV data
df = pd.read_csv("testing.csv")
df['time'] = pd.to_datetime(df['time'])

# Sidebar controls
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date", value=pd.to_datetime("2025-07-23"))
selected_hour = st.sidebar.slider("Select Hour", min_value=0, max_value=23, value=6)
metric = st.sidebar.radio("Pollutant", ["pm25", "pm10"])

# Map style selector
map_style_option = st.sidebar.selectbox("Map Style", ["streets", "light", "dark", "satellite", "satellite-streets"])
map_style = f"mapbox://styles/mapbox/{map_style_option}-v12"

# Filter the data by date and hour
filtered_df = df[(df['time'].dt.date == selected_date) &
                 (df['time'].dt.hour == selected_hour)]

if filtered_df.empty:
    st.warning("No data available for the selected date and time.")
else:
    # Create the pydeck layer
    layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_df,
        get_position='[longitude, latitude]',
        get_weight=metric,
        radiusPixels=60,
        aggregation=pdk.types.String("MEAN"),
    )

    # Set up the view state centered around Delhi
    view_state = pdk.ViewState(
        latitude=filtered_df['latitude'].mean(),
        longitude=filtered_df['longitude'].mean(),
        zoom=10,
        pitch=30,
    )

    # Render the interactive map with map tiles
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=map_style,
        tooltip={"text": f"{metric.upper()}: {{{metric}}} µg/m³"},
    ))
