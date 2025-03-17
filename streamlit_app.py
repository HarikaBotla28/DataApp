import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# Add dropdown for Category
category_selected = st.selectbox('Select a Category', df['Category'].unique())

# Add multi-select for Sub-Category in the selected Category
sub_categories = df[df['Category'] == category_selected]['Sub-Category'].unique()
sub_category_selected = st.multiselect('Select Sub-Categories', sub_categories)

# Filter DataFrame based on selected Sub-Categories
filtered_df = df[(df['Category'] == category_selected) & (df['Sub-Category'].isin(sub_category_selected))]
sales_by_month_filtered = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

# Line chart for sales of selected Sub-Categories
st.line_chart(sales_by_month_filtered, y="Sales")

# Calculate and display metrics for selected items
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin", value=f"{profit_margin:,.2f}%", delta=profit_margin - (df['Profit'] / df['Sales']).mean() * 100)
