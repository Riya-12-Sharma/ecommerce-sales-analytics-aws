import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Analytics", page_icon="📈", layout="wide")
st.title("E-Commerce Sales Analytics")
st.caption("A portfolio dashboard for sales, revenue, product performance, and order trends.")

uploaded = st.file_uploader("Upload orders CSV", type=["csv"])
default_path = os.path.join(os.path.dirname(__file__), "data", "orders.csv")

try:
    df = pd.read_csv(uploaded) if uploaded else pd.read_csv(default_path, parse_dates=["order_date"])
except Exception as exc:
    st.error(f"Could not read CSV: {exc}")
    st.stop()

required = {"order_id", "order_date", "product", "category", "quantity", "unit_price", "region"}
if not required.issubset(df.columns):
    st.error("CSV must contain: " + ", ".join(sorted(required)))
    st.stop()

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
for col in ["quantity", "unit_price"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["order_date", "quantity", "unit_price"])
df["revenue"] = df["quantity"] * df["unit_price"]

st.sidebar.header("Filters")
regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
region = st.sidebar.selectbox("Region", regions)
categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
category = st.sidebar.selectbox("Category", categories)
filtered = df.copy()
if region != "All":
    filtered = filtered[filtered["region"] == region]
if category != "All":
    filtered = filtered[filtered["category"] == category]

total_revenue = filtered["revenue"].sum()
orders = filtered["order_id"].nunique()
units = filtered["quantity"].sum()
aov = total_revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total revenue", f"${total_revenue:,.2f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Units sold", f"{units:,.0f}")
c4.metric("Average order value", f"${aov:,.2f}")

left, right = st.columns(2)
with left:
    daily = filtered.groupby(filtered["order_date"].dt.date, as_index=False)["revenue"].sum()
    daily.columns = ["date", "revenue"]
    st.plotly_chart(px.line(daily, x="date", y="revenue", markers=True, title="Revenue over time"),
                    use_container_width=True)
with right:
    products = filtered.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).head(8)
    st.plotly_chart(px.bar(products, x="revenue", y="product", orientation="h",
                           title="Top products by revenue"), use_container_width=True)

left, right = st.columns(2)
with left:
    category_revenue = filtered.groupby("category", as_index=False)["revenue"].sum()
    st.plotly_chart(px.pie(category_revenue, names="category", values="revenue",
                           title="Revenue by category"), use_container_width=True)
with right:
    region_revenue = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    st.plotly_chart(px.bar(region_revenue, x="region", y="revenue",
                           title="Revenue by region"), use_container_width=True)

st.subheader("Orders data")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True)
st.download_button("Download filtered orders", filtered.to_csv(index=False).encode("utf-8"),
                   "filtered_orders.csv", "text/csv")
