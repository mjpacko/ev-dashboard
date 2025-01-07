import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from utils import load_ev_sales_data
from utils import load_ev_charging_points_data

st.set_page_config(
    page_title="Charging Infrastructure",
    layout="centered",
    page_icon="🔌",
    initial_sidebar_state="expanded"
)

# Load the data
df_charging = load_ev_charging_points_data()

st.title("Charging Infrastructure")
st.markdown("---")

st.subheader("Charging Points by Region")

# Create region selector - only include regions with data
regions = sorted(df_charging[df_charging['value'] > 0]['region'].unique())
selected_region = st.selectbox('Select Region', regions)

# Prepare data for the bar chart, filtered by region
df_region = df_charging[df_charging['region'] == selected_region].groupby('year')['value'].sum().reset_index()

# Create bar chart with trend line
fig = px.bar(
    df_region,
    x='year',
    y='value',
    title=f'Charging Points Evolution - {selected_region}',
    labels={'value': 'Number of Charging Points', 'year': 'Year'},
    color_discrete_sequence=['#004d00']  # Dark green
)

# Add trend line
fig.add_scatter(
    x=df_region['year'],
    y=df_region['value'],
    mode='lines',
    name='Trend',
    line=dict(color='#FF69B4', width=2, dash='dot'),
    showlegend=True
)

# Update layout for better appearance
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=True,
    legend_title_text='',
    height=500,
    yaxis_title='Number of Charging Points',
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

st.subheader("Top Charging Infrastructure by Country 2023")

# Create two columns
col1, col2 = st.columns(2)

# Prepare data for 2023
df_2023 = df_charging[df_charging['year'] == 2023].groupby('region')['value'].sum().reset_index()
df_2023 = df_2023.sort_values('value', ascending=False)

with col1:
    # Create pie chart with custom colors
    fig_pie = px.pie(
        df_2023,
        values='value',
        names='region',
        title='Charging Points Distribution by Country (2023)',
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
    df_display.columns = ['Country', 'Charging Points']
    df_display['Charging Points'] = df_display['Charging Points'].map('{:,.0f}'.format)
    
    # Display simple dataframe
    st.dataframe(
        df_display,
        column_config={
            "Country": st.column_config.TextColumn("Country"),
            "Charging Points": st.column_config.TextColumn("Charging Points")
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

st.markdown("---")
st.subheader("Charging Infrastructure Growth Over Time")

# Create filter for regions
selected_regions = st.multiselect(
    'Select Regions',
    options=regions,
    default=regions[:3]  # Select first 3 regions by default
)

# Filter data based on selections
df_line = df_charging[df_charging['region'].isin(selected_regions)].copy()

# Prepare data for line graph
df_line = df_line.groupby(['year', 'region'])['value'].sum().reset_index()

# Create line graph
fig_line = px.line(
    df_line,
    x='year',
    y='value',
    color='region',
    title='Charging Points Growth by Region',
    labels={'value': 'Number of Charging Points', 'year': 'Year', 'region': 'Region'},
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
    hovertemplate='<b>%{y:,.0f}</b> charging points<extra></extra>'
)

# Display the chart
st.plotly_chart(fig_line, use_container_width=True)
