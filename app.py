import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import time

# Load the data
df = pd.read_csv("testing.csv", parse_dates=["time"])

# Sidebar elements
st.sidebar.title("Air Quality Map Controls")

# Select Date (we only have one in this dataset)
unique_dates = df['time'].dt.date.unique()
selected_date = st.sidebar.date_input("Select date", value=unique_dates[0])

# Select PM type
pm_type = st.sidebar.selectbox("Select PM value", ["pm25", "pm10"])

# Select time with slider
selected_hour = st.sidebar.slider("Select time of selected day", 0, 5, 0)

# Filter data
filtered_df = df[
    (df['time'].dt.date == selected_date) &
    (df['time'].dt.hour == selected_hour)
]

# Page layout
st.title("Air Quality Map")

# Search bar
search_location = st.text_input("Search", "")

# Show predicted interactive map
st.write(f"### PM Concentration at {selected_hour:02d}:00 hrs on {selected_date}")

# Color scale range
min_val = filtered_df[pm_type].min()
max_val = filtered_df[pm_type].max()

# Define layer for pydeck map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[longitude, latitude]',
    get_radius=500,
    get_fill_color=f'[255 * ({pm_type} - {min_val}) / ({max_val - min_val + 1e-6}), 100, 150]',
    pickable=True
)

# Define tooltip
tooltip = {
    "html": f"<b>{pm_type.upper()}</b>: {{{pm_type}}} μg/m³",
    "style": {"color": "white"}
}

# Render pydeck map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=28.6,
        longitude=77.2,
        zoom=9,
        pitch=40
    ),
    layers=[layer],
    tooltip=tooltip
))

# Show data table
with st.expander("Show data table"):
    st.dataframe(filtered_df.reset_index(drop=True))
