import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Insurance Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("insurance.data.aggregated.csv")

    # Rename long column names
    df = df.rename(columns={
        "TotalNumberOfInsurancePoliciesPurchaed": "Policies Purchased",
        "TotalNumberOfInsuranceQuotes": "Insurance Quotes"
    })

    return df


df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("📊 Dashboard Filters")

selected_channels = st.sidebar.multiselect(
    "Marketing Channel",
    options=sorted(df["Marketing Channel"].unique()),
    default=sorted(df["Marketing Channel"].unique())
)

selected_devices = st.sidebar.multiselect(
    "Device Category",
    options=sorted(df["Device Category"].unique()),
    default=sorted(df["Device Category"].unique())
)

filtered_df = df[
    (df["Marketing Channel"].isin(selected_channels)) &
    (df["Device Category"].isin(selected_devices))
]

# ==========================================================
# DASHBOARD TITLE
# ==========================================================

st.title("📊 Insurance Analytics Dashboard")
st.markdown("### Insurance Website Performance Analysis")

st.markdown("---")

# ==========================================================
# KPI CARDS
# ==========================================================

total_users = filtered_df["Users"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_quotes = filtered_df["Insurance Quotes"].sum()
total_policies = filtered_df["Policies Purchased"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Users",
    f"{total_users:,}"
)

col2.metric(
    "💰 Revenue",
    f"${total_revenue:,.2f}"
)

col3.metric(
    "📄 Insurance Quotes",
    f"{total_quotes:,}"
)

col4.metric(
    "🛡 Policies Purchased",
    f"{total_policies:,}"
)

st.markdown("---")

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

revenue_channel = (
    filtered_df
    .groupby("Marketing Channel")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

users_channel = (
    filtered_df
    .groupby("Marketing Channel")["Users"]
    .sum()
    .sort_values(ascending=False)
)

device_revenue = (
    filtered_df
    .groupby("Device Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

highest_revenue_channel = revenue_channel.idxmax()
highest_revenue_value = revenue_channel.max()

most_users_channel = users_channel.idxmax()
most_users_value = users_channel.max()

best_device = device_revenue.idxmax()

st.subheader("📌 Executive Summary")

summary1, summary2, summary3 = st.columns(3)

summary1.success(
    f"""
Highest Revenue Channel

**{highest_revenue_channel}**

Revenue:
${highest_revenue_value:,.2f}
"""
)

summary2.info(
    f"""
Most Users

**{most_users_channel}**

Users:
{most_users_value:,}
"""
)

summary3.warning(
    f"""
Best Performing Device

**{best_device}**
"""
)

st.markdown("---")
# ==========================================================
# CHARTS
# ==========================================================

st.subheader("📈 Dashboard Visualisations")

chart1, chart2 = st.columns(2)

# ----------------------------------------------------------

with chart1:

    revenue_chart = (
        filtered_df.groupby("Marketing Channel")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig1 = px.bar(
        revenue_chart,
        x="Marketing Channel",
        y="Revenue",
        text="Revenue",
        title="Revenue by Marketing Channel"
    )

    fig1.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    fig1.update_layout(
        showlegend=False,
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------------------------------

with chart2:

    users_chart = (
        filtered_df.groupby("Marketing Channel")["Users"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig2 = px.bar(
        users_chart,
        x="Marketing Channel",
        y="Users",
        text="Users",
        title="Users by Marketing Channel",
        color="Users"
    )

    fig2.update_traces(
        textposition="outside"
    )

    fig2.update_layout(
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==========================================================

chart3, chart4 = st.columns(2)

with chart3:

    device_chart = (
        filtered_df.groupby("Device Category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        device_chart,
        names="Device Category",
        values="Revenue",
        title="Revenue by Device"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------------------------

with chart4:

    quote_chart = (
        filtered_df.groupby("Marketing Channel")["Insurance Quotes"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig4 = px.bar(
        quote_chart,
        x="Marketing Channel",
        y="Insurance Quotes",
        text="Insurance Quotes",
        title="Insurance Quotes by Marketing Channel",
        color="Insurance Quotes"
    )

    fig4.update_traces(
        textposition="outside"
    )

    fig4.update_layout(
        height=450
    )

    st.plotly_chart(fig4, use_container_width=True)

# ==========================================================

st.subheader("📊 Revenue vs Session Duration")

fig5 = px.scatter(
    filtered_df,
    x="Avg. Session Duration",
    y="Revenue",
    size="Users",
    color="Marketing Channel",
    hover_name="Marketing Channel"
)

fig5.update_layout(height=600)

st.plotly_chart(fig5, use_container_width=True)

# ==========================================================

with st.expander("📋 View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )