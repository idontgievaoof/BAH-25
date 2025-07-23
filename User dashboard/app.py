import streamlit as st
import pandas as pd
import pydeck as pdk
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Air Quality Monitoring Dashboard",
    page_icon="💨",
    layout="wide",
)


# --- Data Loading ---
# This function loads the data. Caching it makes the app run faster.
@st.cache_data
def load_data():
    # !!! IMPORTANT !!!
    # Replace 'your_final_processed_data.csv' with the actual filename of your dataset.
    # Make sure your CSV has columns named 'latitude', 'longitude', 'time', 'pm25', and 'pm10'.
    # The 'time' column should be a datetime object.
    try:
        df = pd.read_csv('testing.csv')
        df['time'] = pd.to_datetime(df['time'])
        return df
    except FileNotFoundError:
        # Create a sample DataFrame if the file isn't found, so the app doesn't crash.
        st.error("Data file not found. Displaying sample data.")
        sample_data = {
            'time': pd.to_datetime(['2023-01-15T10:00:00', '2023-01-15T11:00:00']),
            'latitude': [30.73, 30.74],
            'longitude': [76.77, 76.78],
            'pm25': [85.5, 92.1],
            'pm10': [150.2, 165.7]
        }
        return pd.DataFrame(sample_data)

df = load_data()


# --- Sidebar for Controls ---
st.sidebar.header("Controls")

# Date selector
selected_date = st.sidebar.date_input(
    "Select date",
    datetime.date(2023, 1, 15), # Default date
    min_value=df['time'].min().date(),
    max_value=df['time'].max().date()
)

# PM value selector
pm_type = st.sidebar.selectbox(
    "Select PM value",
    ('PM2.5', 'PM10')
)
# Map the selection to the column name in the DataFrame
pm_column = 'pm25' if pm_type == 'PM2.5' else 'pm10'

# Time slider
selected_hour = st.sidebar.slider(
    "Select time of selected day",
    0, 23, 10  # Min, max, default value
)


# --- Filtering Data Based on Controls ---
# Combine date and time to create a full datetime object for filtering
filter_time = pd.to_datetime(f"{selected_date} {selected_hour:02d}:00:00")

# Find the closest timestamp in the data
filtered_df = df.iloc[(df['time'] - filter_time).abs().argsort()[:1]]


# --- Main Panel ---
st.header("Air Quality Map")

# Define the PyDeck map layer
layer = pdk.Layer(
    'ScatterplotLayer',
    data=filtered_df,
    get_position='[longitude, latitude]',
    get_color=f'[255, 140, 0, 160]',  # Using a single color for now
    get_radius=f'{pm_column} * 100', # Radius based on PM value
    pickable=True,
    auto_highlight=True
)

# Define the tooltip that appears on hover
tooltip = {
    "html": f"<b>PM Value:</b> {{{pm_column}}} µg/m³<br/><b>Time:</b> {{time}}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white"
    }
}

# Define the initial view of the map
view_state = pdk.ViewState(
    latitude=30.7,
    longitude=76.7,
    zoom=8,
    pitch=50
)

# Render the map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip
))

st.write(f"Displaying data for **{pm_type}** on **{selected_date.strftime('%Y-%m-%d')}** at approximately **{selected_hour:02d}:00**.")
