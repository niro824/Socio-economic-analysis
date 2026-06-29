import streamlit as st

st.title('Sri Lanka socio economic analysis')

st.write("Let's analyze")
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Sri Lanka Socio-Economic Analysis", layout="wide")

# 2. Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv("Sri lanka master data.csv")
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Dashboard Filters")

# Filter out rows that represent aggregated province totals, keeping only individual districts
district_df = df[df['Region_Level'] == 'District']

# Multi-select dropdown for Districts
all_districts = sorted(district_df['District'].unique())
selected_districts = st.sidebar.multiselect(
    "Select Districts:", 
    options=all_districts, 
    default=["Colombo", "Gampaha", "Kalutara"]  # Matches your screen options
)

# Filter the dataset dynamically based on selected districts
filtered_df = district_df[district_df['District'].isin(selected_districts)]

# 4. Main App Layout
st.title('📊 Sri Lanka Socio-Economic Analysis')
st.write("Analyze and compare historical trends across different districts.")

# Create tabs to organize content
tab1, tab2 = st.tabs(["📈 Visualizations", "📋 Data View"])

with tab1:
    st.subheader("Interactive Trend Chart")
    
    # Dynamic Indicator Selection: Let users choose what to plot on the Y-axis
    available_indicators = [
        "LFPR_Total", "LFPR_Male", "LFPR_Female", 
        "Unemployment_Rate", "Mid_Year_Population", 
        "Birth_Rate", "Death_Rate"
    ]
    
    selected_indicator = st.selectbox(
        "Choose an economic indicator to plot:", 
        options=available_indicators
    )
    
    # Generate the line chart dynamically using the selected metric
    if not filtered_df.empty:
        fig = px.line(
            filtered_df, 
            x="Year", 
            y=selected_indicator, 
            color="District", 
            markers=True,
            title=f"Trend of {selected_indicator.replace('_', ' ')} Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one district from the sidebar to view the chart.")

with tab2:
    st.subheader("Filtered Dataset Table")
    st.dataframe(filtered_df)
