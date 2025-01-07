import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from utils import load_ev_sales_data
from utils import load_ev_charging_points_data

st.set_page_config(
    page_title="EV Sales by Region",
    layout="centered",
    page_icon="🌎",
    initial_sidebar_state="expanded"
)

# Load the data
df_ev_sales = load_ev_sales_data()
df_charging = load_ev_charging_points_data()

st.title("EV Sales Data")
st.markdown("---")

st.subheader("EV sales by region")

# Create region selector - only include regions with data
regions = sorted(df_ev_sales[df_ev_sales['value'] > 0]['region'].unique())
selected_region = st.selectbox('Select Region', regions)

# Prepare data for the stacked bar chart, filtered by region
df_stacked = df_ev_sales[df_ev_sales['region'] == selected_region].pivot_table(
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
    title=f'EV Sales by Powertrain Type - {selected_region}',
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
st.markdown("---")

st.subheader("Top Sales by Country 2023")

# Create two columns
col1, col2 = st.columns(2)

# Prepare data for 2023
df_2023 = df_ev_sales[df_ev_sales['year'] == 2023].groupby('region')['value'].sum().reset_index()
df_2023 = df_2023.sort_values('value', ascending=False)

with col1:
    # Create pie chart with custom colors
    fig_pie = px.pie(
        df_2023,
        values='value',
        names='region',
        title='EV Sales Distribution by Country (2023)',
        hole=0.3,
        color_discrete_sequence=['#004d00', '#00b300', '#80ff80', '#e6fff2', '#ccffeb', '#b3ffe6', '#99ffe0', '#80ffdb', '#66ffd6']
    )
    
    # Update pie chart layout
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Remove values from the pie chart and update hover info
    fig_pie.update_traces(
        textposition='none',
        hovertemplate="<b>%{label}</b><br>%{percent:.1%}<extra></extra>"
    )
    
    # Display pie chart
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Prepare dataframe for display
    df_display = df_2023.copy()
    df_display.columns = ['Country', 'Cars Sold']
    df_display['Cars Sold'] = df_display['Cars Sold'].map('{:,.0f}'.format)
    
    # Display simple dataframe without selection
    st.dataframe(
        df_display,
        column_config={
            "Country": st.column_config.TextColumn("Country"),
            "Cars Sold": st.column_config.TextColumn("Cars Sold")
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

st.markdown("---")
st.subheader("Sales Trends Over Time")

# Create filters
col_filters1, col_filters2 = st.columns(2)

with col_filters1:
    selected_regions = st.multiselect(
        'Select Regions',
        options=regions,
        default=regions[:3]  # Select first 3 regions by default
    )

with col_filters2:
    selected_powertrain = st.selectbox(
        'Select Powertrain',
        options=['All'] + list(df_ev_sales['powertrain'].unique())
    )

# Filter data based on selections
df_line = df_ev_sales.copy()

# Filter by selected regions
df_line = df_line[df_line['region'].isin(selected_regions)]

# Filter by powertrain if not 'All'
if selected_powertrain != 'All':
    df_line = df_line[df_line['powertrain'] == selected_powertrain]

# Prepare data for line graph
if selected_powertrain == 'All':
    df_line = df_line.groupby(['year', 'region'])['value'].sum().reset_index()
else:
    df_line = df_line.groupby(['year', 'region'])['value'].sum().reset_index()

# Create line graph
fig_line = px.line(
    df_line,
    x='year',
    y='value',
    color='region',
    title=f'{selected_powertrain} Sales Trends by Region',
    labels={'value': 'Cars Sold', 'year': 'Year', 'region': 'Region'},
    color_discrete_sequence=['#004d00', '#006600', '#008000', '#009900', '#00b300', '#00cc00', '#00e600', '#00ff00', '#1aff1a']
)

# Update layout
fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=500,
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ),
    yaxis=dict(
        gridcolor='rgba(128,128,128,0.1)',
        zerolinecolor='rgba(128,128,128,0.1)'
    ),
    xaxis=dict(
        gridcolor='rgba(128,128,128,0.1)',
        zerolinecolor='rgba(128,128,128,0.1)'
    ),
    hovermode='x unified'
)

# Update line properties
fig_line.update_traces(
    mode='lines+markers',
    hovertemplate='<b>%{y:,.0f}</b> cars<extra></extra>'
)

# Display the chart
st.plotly_chart(fig_line, use_container_width=True)