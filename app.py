import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("testing.csv")  # Replace with your CSV file path
    return df

df = load_data()

# Sidebar: Select timestamp
available_times = df['time'].unique()
selected_time = st.sidebar.selectbox("Select Time", available_times)

# Filter for selected time
filtered = df[df['time'] == selected_time]

# Pivot for heatmap
heatmap_data = filtered.pivot(index='y', columns='x', values='pm_concentration')
heatmap_data = heatmap_data.sort_index(ascending=False)  # Y-axis inversion

# Plot heatmap
fig = px.imshow(
    heatmap_data,
    labels=dict(color="PM Concentration"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale='YlOrRd',
    origin='upper',
    aspect='auto'
)

# Smaller squares via layout tuning
fig.update_traces(hovertemplate='x: %{x}<br>y: %{y}<br>PM: %{z:.2f}')
fig.update_layout(
    title=f"PM Concentration Heatmap at {selected_time}",
    xaxis_title="X",
    yaxis_title="Y",
    width=700,
    height=700
)

# Display
st.title("📊 Heatmap Viewer")
st.plotly_chart(fig, use_container_width=True)
