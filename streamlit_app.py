import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")

# Load dataset
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])  # Ensure Order_Date is parsed correctly

# Ensure column names have no leading/trailing spaces
df.columns = df.columns.str.strip()

st.dataframe(df)

# Bar chart without aggregation
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart
aggregated_df = df.groupby("Category", as_index=False).sum()
st.dataframe(aggregated_df)
st.bar_chart(aggregated_df, x="Category", y="Sales", color="#04f")

# Aggregating sales by month
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors='coerce')  # Ensure correct datetime format, handle errors
df.dropna(subset=["Order_Date"], inplace=True)  # Drop rows with invalid dates
df.set_index("Order_Date", inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1) Dropdown for Category Selection
if "Category" in df.columns:
    categories = df["Category"].dropna().unique()
    selected_category = st.selectbox("Select a Category:", categories, key="category_select")
else:
    st.error("Column 'Category' not found in the dataset.")
    selected_category = None

# (2) Multi-select for Sub-Category based on selected Category
if selected_category and "Sub-Category" in df.columns:
    sub_categories = df[df["Category"] == selected_category]["Sub-Category"].dropna().unique()
    selected_sub_categories = st.multiselect("Select Sub-Categories:", sub_categories, key="sub_category_select")
else:
    selected_sub_categories = []

if selected_sub_categories:
    filtered_df = df[(df["Category"] == selected_category) & (df["Sub-Category"].isin(selected_sub_categories))]
    
    # (3) Line chart of sales for selected items
    if not filtered_df.empty:
        sales_by_month_filtered = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
        st.line_chart(sales_by_month_filtered, y="Sales")
    else:
        st.warning("No data available for the selected filters.")
    
    # (4) Metrics: Total Sales, Total Profit, Overall Profit Margin
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0
    
    # (5) Overall Profit Margin Comparison
    overall_sales = df["Sales"].sum()
    overall_profit = df["Profit"].sum()
    overall_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales else 0
    delta_margin = profit_margin - overall_profit_margin
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")
