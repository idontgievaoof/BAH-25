import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime

# Set up the app
st.set_page_config(page_title="Air Quality Map", layout="wide")
st.title("Delhi Air Quality Grid: PM₂.₅ and PM₁₀ Interactive Map")

# Upload or load CSV data
df = pd.read_csv("testing.csv")
df['time'] = pd.to_datetime(df['time'])

# Sidebar controls
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select Date", value=pd.to_datetime("2025-07-23"))
selected_hour = st.sidebar.slider("Select Hour", min_value=0, max_value=23, value=5)
metric = st.sidebar.radio("Pollutant", ["pm25", "pm10"])

# Filter the data by date and selected hour
filtered_df = df[(df['time'].dt.date == selected_date) &
                 (df['time'].dt.hour == selected_hour)]

if filtered_df.empty:
    st.warning("No data available for the selected date and time.")
else:
    # Drop NaNs for cleaner display
    filtered_df = filtered_df.dropna(subset=[metric])

    # Create PyDeck layer for scatterplot
    layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_df,
        get_position='[longitude, latitude]',
        get_weight=metric,
        radiusPixels=40,
        aggregation='MEAN'
    )

    tooltip = {
        "html": f"<b>PM Concentration:</b> {{{metric}}} μg/m³",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # Display PyDeck map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(
            latitude=filtered_df['latitude'].mean(),
            longitude=filtered_df['longitude'].mean(),
            zoom=10,
            pitch=40,
        ),
        layers=[layer],
        tooltip=tooltip
    ))
