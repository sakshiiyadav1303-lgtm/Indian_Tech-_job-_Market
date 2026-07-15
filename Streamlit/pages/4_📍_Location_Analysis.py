import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Location Analysis",
    page_icon="📍",
    layout="wide"
)

st.title("📍 Location Analysis")

st.markdown(
"""
Explore hiring patterns, salaries and work modes across Indian cities.
"""
)

st.markdown("---")

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

salary_df = df[
    (df["salary_disclosed"] == True)
    &
    (df["salary_midpoint_lpa"].notna())
].copy()

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🎯 Filters")

selected_work = st.sidebar.multiselect(
    "🏠 Work Mode",
    sorted(salary_df["work_mode"].dropna().unique())
)

selected_exp = st.sidebar.multiselect(
    "👨‍💻 Experience",
    sorted(salary_df["experience_tier"].dropna().unique())
)

filtered_df = salary_df.copy()

if selected_work:

    filtered_df = filtered_df[
        filtered_df["work_mode"].isin(selected_work)
    ]

if selected_exp:

    filtered_df = filtered_df[
        filtered_df["experience_tier"].isin(selected_exp)
    ]

if filtered_df.empty:

    st.warning(
        "⚠ No data found for selected filters."
    )

    st.stop()

# ==========================================
# KPI CARDS
# ==========================================

st.subheader("📊 Location Overview")

total_cities = filtered_df["primary_city"].nunique()

top_city = (
    filtered_df["primary_city"]
    .value_counts()
    .idxmax()
)

highest_city = (
    filtered_df
    .groupby("primary_city")["salary_midpoint_lpa"]
    .mean()
    .idxmax()
)

avg_salary = (
    filtered_df["salary_midpoint_lpa"]
    .mean()
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "📍 Cities",
    total_cities
)

k2.metric(
    "🏆 Most Hiring City",
    top_city
)

k3.metric(
    "💰 Highest Paying City",
    highest_city
)

k4.metric(
    "📈 Avg Salary",
    f"{avg_salary:.2f} LPA"
)

st.markdown("---")
# ==========================================
# CITY ANALYSIS
# ==========================================

left, right = st.columns(2)

# ==========================================
# LEFT : TOP HIRING CITIES
# ==========================================

with left:

    st.subheader("🏙 Top Hiring Cities")

    hiring = (
        filtered_df["primary_city"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    hiring.columns = ["City", "Jobs"]

    fig = px.bar(
        hiring,
        x="Jobs",
        y="City",
        orientation="h",
        color="Jobs",
        text="Jobs",
        template="plotly_white"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# RIGHT : HIGHEST PAYING CITIES
# ==========================================

with right:

    st.subheader("💰 Highest Paying Cities")

    salary_city = (
        filtered_df
        .groupby("primary_city")["salary_midpoint_lpa"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    salary_city.columns = ["City", "Average Salary"]

    fig = px.bar(
        salary_city,
        x="Average Salary",
        y="City",
        orientation="h",
        color="Average Salary",
        text="Average Salary",
        template="plotly_white"
    )

    fig.update_traces(texttemplate="%{text:.1f}")

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

st.subheader("💡 City Insights")

c1, c2 = st.columns(2)

highest_salary_city = salary_city.iloc[0]
most_hiring_city = hiring.iloc[0]

with c1:

    st.success(
        f"""
🏆 Highest Paying City

**{highest_salary_city['City']}**

Average Salary:
**{highest_salary_city['Average Salary']:.2f} LPA**
"""
    )

with c2:

    st.info(
        f"""
📍 Most Hiring City

**{most_hiring_city['City']}**

Jobs Posted:
**{most_hiring_city['Jobs']}**
"""
    )
st.markdown("---")

st.subheader("🏠 Work Mode Distribution")

work_mode = (
    filtered_df["work_mode"]
    .value_counts()
    .reset_index()
)

work_mode.columns = ["Work Mode", "Jobs"]

fig = px.pie(
    work_mode,
    values="Jobs",
    names="Work Mode",
    hole=0.5,
    title="Work Mode Distribution"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("👨‍💻 Experience Level Distribution")

experience = (
    filtered_df["experience_tier"]
    .value_counts()
    .reset_index()
)

experience.columns = ["Experience", "Jobs"]

fig = px.bar(
    experience,
    x="Experience",
    y="Jobs",
    color="Jobs",
    text="Jobs",
    template="plotly_white"
)

fig.update_layout(
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="location_analysis.csv",
    mime="text/csv"
)