import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

# Load the data (make sure to keep this CSV in the same directory)
df = pd.read_csv("delhi_air_quality_grid.csv", parse_dates=['time'])

# App layout
st.set_page_config(page_title="Air Quality Grid Viewer", layout="wide")
st.title("Delhi NCR Air Quality Grid (Midnight - 6 AM)")
st.markdown("""
This map displays interpolated PM₂.₅ and PM₁₀ levels over the Delhi NCR region.
Select a date, PM type, and hour to view pollution concentrations.
""")

# Sidebar controls with light theme look
with st.sidebar:
    st.header("Controls")
    selected_date = st.date_input("Select Date", value=date.today())
    pm_type = st.selectbox("Select PM Type", ["pm25", "pm10"])
    hour = st.slider("Hour of Day (0 to 6 only)", 0, 6, 3)

# Filter based on date and hour
df_today = df[df['time'].dt.date == selected_date]

df_filtered = df_today[df_today['time'].dt.hour == hour]

if df_filtered.empty:
    st.warning("No data available for the selected date and time.")
else:
    # Setup color range
    color_range = {
        "pm25": [0, 250],
        "pm10": [0, 300]
    }

    fig = go.Figure(go.Densitymapbox(
        lat=df_filtered['latitude'],
        lon=df_filtered['longitude'],
        z=df_filtered[pm_type],
        radius=30,
        colorscale="YlOrRd",
        zmin=color_range[pm_type][0],
        zmax=color_range[pm_type][1],
        hovertemplate=
            "Latitude: %{lat}<br>" +
            "Longitude: %{lon}<br>" +
            f"{pm_type.upper()} = %{{z}} µg/m³"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=dict(lat=28.6, lon=77.2),
            zoom=9,
            pitch=0,
            bearing=0
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=650,
        coloraxis_showscale=True
    )

    st.plotly_chart(fig, use_container_width=True)
