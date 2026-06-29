import streamlit as st

st.title('Sri Lanka socio economic analysis')

st.write("Let's analyze")
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration (Matches the clean layout of image_daa0e0.jpg)
st.set_page_config(page_title="Sri Lanka Subnational Disparities Explorer", layout="wide")

# 2. Cached Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv("Sri lanka master data.csv")
    return df

df = load_data()

# Clean data: Filter out province summaries, evaluate pure subnational districts
district_df = df[df['Region_Level'] == 'District'].copy()

# 3. Sidebar Panel (Replicating the 'Inequality Explorer' structure from image_daa0e0.jpg)
st.sidebar.title("Subnational Disparities")
st.sidebar.markdown("*GSID Regional Analytics Framework*")

# Section Navigation
section = st.sidebar.radio(
    "Section Navigation",
    ["Overview & Metrics", "Distribution Dynamics", "Spatial Relationships", "Raw Panel Data"]
)

# Indicator Variable Selection
available_metrics = [
    "LFPR_Total", "LFPR_Male", "LFPR_Female", 
    "Unemployment_Rate", "Mid_Year_Population", 
    "Birth_Rate", "Death_Rate"
]
selected_metric = st.sidebar.selectbox("Socio-Economic Variable:", available_metrics)

# Dynamic Year Selection Panel
available_years = sorted(district_df['Year'].unique())
selected_year = st.sidebar.select_slider("Select Target Year:", options=available_years, value=available_years[-1])

# Dynamic District Multi-selector
all_districts = sorted(district_df['District'].unique())
selected_districts = st.sidebar.multiselect(
    "Select Districts to Analyze:", 
    options=all_districts, 
    default=all_districts[:6]
)

# Apply Filters
year_df = district_df[district_df['Year'] == selected_year]
filtered_df = district_df[
    (district_df['District'].isin(selected_districts))
]

# 4. Main Display Layout Logic
st.title("Sri Lanka Subnational Development Explorer")
st.markdown(f"**Current Variable:** `{selected_metric}` | **Analytic Framework:** Spatial Variations & Convergence")

# --- SECTION 1: OVERVIEW & METRICS ---
if section == "Overview & Metrics":
    st.subheader(f"Regional Disparities Overview ({selected_year})")
    
    # Calculate real-time convergence/disparity statistics
    avg_val = year_df[selected_metric].mean()
    std_val = year_df[selected_metric].std()
    cv_val = std_val / avg_val if avg_val != 0 else 0  # Coefficient of Variation (Sigma Disparity metric)
    
    # Display Analytic Cards (Replicating summary rows from image_daa0e0.jpg)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Observed Districts", f"{year_df['District'].nunique()}")
    c2.metric("National Mean", f"{avg_val:,.2f}")
    c3.metric("Standard Deviation (Absolute Disparity)", f"{std_val:.4f}")
    c4.metric("Coef. of Variation (Sigma Inequality)", f"{cv_val:.4f}")
    
    # Comparative Visual Analysis
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown(f"#### Rank-Ordered Regional Disparities ({selected_year})")
        sorted_year_df = year_df.sort_values(by=selected_metric, ascending=False)
        fig_bar = px.bar(
            sorted_year_df, x="District", y=selected_metric,
            color=selected_metric, color_continuous_scale="Viridis",
            labels={selected_metric: selected_metric.replace('_', ' ')}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### Longitudinal Structural Trend Paths")
        if not filtered_df.empty:
            fig_line = px.line(
                filtered_df, x="Year", y=selected_metric, color="District", 
                markers=True, line_shape="linear"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("Select districts in the sidebar to generate longitudinal paths.")

# --- SECTION 2: DISTRIBUTION DYNAMICS ---
elif section == "Distribution Dynamics":
    st.subheader("Subnational Distribution Dynamics & Spread")
    st.markdown("Analyzing changes in the shape and spread of distributions over time provides insights into whether districts are converging or polarizing.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### Box & Whiskers Spread Profile ({selected_year})")
        fig_box = px.box(year_df, y=selected_metric, points="all", hover_data=["District"], color_discrete_sequence=["#1f77b4"])
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col2:
        st.markdown("#### Structural Evolution Across Cross-Sections")
        fig_hist = px.histogram(
            district_df, x=selected_metric, color="Year", 
            marginal="rug", barmode="overlay", opacity=0.7
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# --- SECTION 3: SPATIAL RELATIONSHIPS ---
elif section == "Spatial Relationships":
    st.subheader("Variable Correlation & Development Regimes")
    st.markdown("Explores how economic metrics correlate across districts to reveal structural patterns.")
    
    # Compute correlation matrix dynamically for numeric metrics
    corr_df = year_df[available_metrics].corr()
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown("#### Core Indicator Correlation Matrix")
        fig_heat = px.imshow(
            corr_df, text_auto=".2f", 
            color_continuous_scale="RdBu_r", zmin=-1, zmax=1
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col2:
        st.markdown("#### Multi-Dimensional Trade-off Matrix")
        x_var = st.selectbox("Select X Axis Indicator:", available_metrics, index=0)
        y_var = st.selectbox("Select Y Axis Indicator:", available_metrics, index=3)
        
        fig_scatter = px.scatter(
            year_df, x=x_var, y=y_var, text="District", color="Province",
            size="Mid_Year_Population" if "Mid_Year_Population" in year_df.columns else None,
            title=f"{x_var} vs {y_var} Matrix across Regimes"
        )
        fig_scatter.update_traces(textposition='top center')
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- SECTION 4: RAW PANEL DATA ---
elif section == "Raw Panel Data":
    st.subheader("Subnational Panel Dataset View")
    st.markdown("Interactive table view allowing custom data sorting, extraction, and downloading for empirical modeling packages.")
    
    st.dataframe(filtered_df if not filtered_df.empty else district_df, use_container_width=True)
    
    csv = (filtered_df if not filtered_df.empty else district_df).to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Structured Panel CSV Data",
        data=csv,
        file_name="srilanka_subnational_filtered_panel.csv",
        mime="text/csv"
    )
# --- SECTION 3: SPATIAL RELATIONSHIPS ---
elif section == "Spatial Relationships":
    st.subheader("Variable Correlation & Development Regimes")
    st.markdown("Explores how economic metrics correlate across districts to reveal structural patterns.")
    
    # DYNAMIC FIX: Only use numeric columns that actually exist in your dataset
    existing_metrics = [metric for metric in available_metrics if metric in year_df.columns]
    
    if len(existing_metrics) > 1:
        # Compute correlation matrix dynamically safely
        corr_df = year_df[existing_metrics].corr()
        
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("#### Core Indicator Correlation Matrix")
            fig_heat = px.imshow(
                corr_df, text_auto=".2f", 
                color_continuous_scale="RdBu_r", zmin=-1, zmax=1
            )
            st.plotly_chart(fig_heat, use_container_width=True)
            
        with col2:
            st.markdown("#### Multi-Dimensional Trade-off Matrix")
            x_var = st.selectbox("Select X Axis Indicator:", existing_metrics, index=0)
            y_var = st.selectbox("Select Y Axis Indicator:", existing_metrics, index=min(3, len(existing_metrics)-1))
            
            fig_scatter = px.scatter(
                year_df, x=x_var, y=y_var, text="District", color="Province",
                size="Mid_Year_Population" if "Mid_Year_Population" in year_df.columns else None,
                title=f"{x_var} vs {y_var} Matrix"
            )
            fig_scatter.update_traces(textposition='top center')
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.error("Not enough matching numeric columns found in the CSV to calculate correlations. Please check your column headers.")
