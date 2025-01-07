import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from utils import load_ev_sales_data
from utils import load_ev_charging_points_data

st.set_page_config(
    page_title="EV Adoption Tracker",
    layout="centered",
    page_icon="🚗",
    initial_sidebar_state="expanded"
)

# Load the data
df_ev_sales = load_ev_sales_data()
df_charging = load_ev_charging_points_data()

# Calculate EV sales metrics
latest_year = df_ev_sales['year'].max()
total_sales = df_ev_sales[df_ev_sales['year'] == latest_year]['value'].sum()
previous_year_sales = df_ev_sales[df_ev_sales['year'] == latest_year - 1]['value'].sum()
sales_change = total_sales - previous_year_sales

# Calculate growth percentage
growth_percentage = ((total_sales - previous_year_sales) / previous_year_sales) * 100
previous_growth = ((previous_year_sales - df_ev_sales[df_ev_sales['year'] == latest_year - 2]['value'].sum()) 
                  / df_ev_sales[df_ev_sales['year'] == latest_year - 2]['value'].sum()) * 100
growth_change = growth_percentage - previous_growth

# Calculate charging points metrics
total_charging = df_charging[df_charging['year'] == latest_year]['value'].sum()
previous_charging = df_charging[df_charging['year'] == latest_year - 1]['value'].sum()
charging_change = total_charging - previous_charging

# Format the numbers
def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

# Format percentage with + or - sign
def format_percentage(pct):
    return f"{'+' if pct > 0 else ''}{pct:.1f}%"

st.title("EV Adoption Tracker")
st.subheader("Summary")
st.text("This is a summary of the EV Adoption Tracker data from the IEA. With this app you can explore historical and projected data on electric vehicles sales and charging infrastructure.")

with st.expander("Click here to learn more about this dataset"):
    st.write("""
        This dataset was complied from the IEA's EV Sales and Charging Points datasets.
            
The Global EV Outlook is an annual publication that identifies and discusses recent developments in electric mobility across the globe. It is developed with the support of the members of the Electric Vehicles Initiative (EVI).

Combining historical analysis with projections to 2030, the report examines key areas of interest such as electric vehicle and charging infrastructure deployment, energy use, CO2 emissions, battery demand and related policy developments. The report includes policy recommendations that incorporate lessons learned from leading markets to inform policy makers and stakeholders with regard to policy frameworks and market systems for electric vehicle adoption.

    """)

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="World EV Sales",
        value=format_number(total_sales),
        delta=format_number(sales_change)
    )

with col2:
    st.metric(
        label="Sales Growth Rate",
        value=format_percentage(growth_percentage),
        delta=format_percentage(growth_change)
    )

with col3:
    st.metric(
        label="Charging Points",
        value=format_number(total_charging),
        delta=format_number(charging_change)
    )


st.subheader("Total units sold over time by Region")

# Prepare data for the stacked bar chart (no region filter)
df_stacked = df_ev_sales.pivot_table(
    index='year',
    columns='powertrain',
    values='value',
    aggfunc='sum'
).reset_index()

# Calculate total for each year
df_stacked['Total'] = df_stacked[['BEV', 'PHEV', 'FCEV']].sum(axis=1)

# Create color map with different shades of green
color_map = {
    'BEV': '#004d00',  # Dark green
    'PHEV': '#00b300',  # Medium green
    'FCEV': '#80ff80'   # Light green
}

# Create stacked bar chart with trend line
fig = px.bar(
    df_stacked,
    x='year',
    y=['BEV', 'PHEV', 'FCEV'],
    title='Global EV Sales by Powertrain Type',
    labels={'value': 'Units Sold', 'year': 'Year', 'variable': 'Powertrain Type'},
    color_discrete_map=color_map
)

# Add trend line
fig.add_scatter(
    x=df_stacked['year'],
    y=df_stacked['Total'],
    mode='lines',
    name='Total Trend',
    line=dict(color='#FF69B4', width=2, dash='dot'),
    showlegend=True
)

# Update layout for better appearance
fig.update_layout(
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    legend_title_text='Powertrain Type',
    height=500,
    yaxis_title='Units Sold',
    xaxis_title='Year',
    yaxis=dict(
        gridcolor='rgba(128,128,128,0.1)',
        zerolinecolor='rgba(128,128,128,0.1)'
    ),
    xaxis=dict(
        gridcolor='rgba(128,128,128,0.1)',
        zerolinecolor='rgba(128,128,128,0.1)'
    )
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)