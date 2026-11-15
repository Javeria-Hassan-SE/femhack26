import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Simple Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Generate synthetic sales data
@st.cache_data
def generate_synthetic_data(num_records=500):
    np.random.seed(42)
    
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Beauty"]
    regions = ["North", "South", "East", "West"]
    
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    
    dates = [
        start_date + timedelta(days=int(np.random.randint(0, 91)))
        for _ in range(num_records)
    ]
    
    data = {
        "Order_ID": [f"ORD-{1000 + i}" for i in range(num_records)],
        "Date": pd.to_datetime(dates),
        "Category": np.random.choice(categories, size=num_records, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        "Region": np.random.choice(regions, size=num_records),
        "Units_Sold": np.random.randint(1, 10, size=num_records),
        "Unit_Price": np.random.choice([15.0, 25.0, 50.0, 120.0, 250.0, 450.0], size=num_records),
    }
    
    df = pd.DataFrame(data)
    df["Total_Sales"] = df["Units_Sold"] * df["Unit_Price"]
    df = df.sort_values(by="Date").reset_index(drop=True)
    return df

# Load data
df = generate_synthetic_data()

# Header
st.title("📊 Simple Sales Dashboard")
st.markdown("A clean and simple sales performance dashboard powered by synthetic data.")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Region filter
all_regions = ["All"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", all_regions)

# Category filter
all_categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", all_categories)

# Apply filters
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# KPI Metrics
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Total_Sales"].sum()
total_units = filtered_df["Units_Sold"].sum()
total_orders = len(filtered_df)
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

with col1:
    st.metric(label="Total Revenue", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Units Sold", value=f"{total_units:,}")
with col3:
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col4:
    st.metric(label="Avg Order Value", value=f"${avg_order_value:,.2f}")

st.divider()

# Charts
st.subheader("Sales Trends & Breakdown")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Daily Sales Trend**")
    daily_sales = (
        filtered_df.groupby("Date")["Total_Sales"]
        .sum()
        .reset_index()
        .set_index("Date")
    )
    st.line_chart(daily_sales)

with chart_col2:
    st.markdown("**Sales by Category**")
    category_sales = (
        filtered_df.groupby("Category")["Total_Sales"]
        .sum()
        .reset_index()
        .set_index("Category")
    )
    st.bar_chart(category_sales)

st.divider()

# Regional Breakdown & Data Table
st.subheader("Regional Performance & Recent Orders")
tab1, tab2 = st.tabs(["Sales by Region", "Raw Data Preview"])

with tab1:
    region_sales = (
        filtered_df.groupby("Region")["Total_Sales"]
        .sum()
        .reset_index()
        .set_index("Region")
    )
    st.bar_chart(region_sales)

with tab2:
    st.dataframe(
        filtered_df[["Order_ID", "Date", "Category", "Region", "Units_Sold", "Unit_Price", "Total_Sales"]],
        hide_index=True
    )
