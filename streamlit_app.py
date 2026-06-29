import streamlit as st

st.title('Sri Lanka socio economic analysis')

st.write('let's analyze')
# ==========================================
# PART 1: IMPORTS (Always at the very top)
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PART 2: PAGE CONFIG & DATA LOADING
# ==========================================
st.set_page_config(page_title="Socio-economic Dashboard", layout="wide")

@st.cache_data
def load_data():
    # This loads the CSV file shown in your GitHub repository screenshot
    df = pd.read_csv("Sri lanka master data.csv")
    return df

df = load_data()

# ==========================================
# PART 3: SIDEBAR FILTERS (Interactive controls)
# ==========================================
st.sidebar.header("Dashboard Filters")

# Example: Dropdown selector for districts
all_districts = df['District'].unique() # Change 'District' to your CSV's column name
selected_districts = st.sidebar.multiselect(
    "Select Districts:", 
    options=all_districts, 
    default=all_districts[:3]
)

# Filter the dataset dynamically based on user selection
filtered_df = df[df['District'].isin(selected_districts)]

# ==========================================
# PART 4: MAIN DISPLAY (Charts, Metrics & Tables)
# ==========================================
st.title("📊 Sri Lanka Socio-economic Dashboard")

# Create tabs to neatly organize your layout
tab1, tab2 = st.tabs(["📈 Visualizations", "📋 Data View"])

with tab1:
    st.subheader("Interactive Trend Chart")
    # Generate an interactive line chart using Plotly
    # (Make sure 'Year' and 'Value' match columns in your actual CSV file)
    fig = px.line(filtered_df, x="Year", y="Value", color="District", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Filtered Dataset Table")
    st.dataframe(filtered_df)
