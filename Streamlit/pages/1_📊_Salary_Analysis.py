import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Salary Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Salary Analysis Dashboard")
st.markdown(
    "Explore salary trends using only jobs with disclosed salary information."
)

st.markdown("---")

# ---------------------------------------
# Load Data
# ---------------------------------------

df = load_data()

# ---------------------------------------
# Keep only disclosed salaries
# ---------------------------------------

salary_df = df[
    (df["salary_disclosed"] == True)
    & (df["salary_midpoint_lpa"].notna())
].copy()

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------

st.sidebar.header("🎯 Filters")

cities = sorted(salary_df["primary_city"].dropna().unique())

experience = sorted(salary_df["experience_tier"].dropna().unique())

salary_tier = sorted(salary_df["salary_tier"].dropna().unique())

work_mode = sorted(salary_df["work_mode"].dropna().unique())

selected_city = st.sidebar.multiselect(
    "📍 City",
    cities
)

selected_exp = st.sidebar.multiselect(
    "👨‍💻 Experience",
    experience
)

selected_salary = st.sidebar.multiselect(
    "💰 Salary Tier",
    salary_tier
)

selected_work = st.sidebar.multiselect(
    "🏠 Work Mode",
    work_mode
)

# ---------------------------------------
# Apply Filters
# ---------------------------------------

filtered_df = salary_df.copy()

if selected_city:
    filtered_df = filtered_df[
        filtered_df["primary_city"].isin(selected_city)
    ]

if selected_exp:
    filtered_df = filtered_df[
        filtered_df["experience_tier"].isin(selected_exp)
    ]

if selected_salary:
    filtered_df = filtered_df[
        filtered_df["salary_tier"].isin(selected_salary)
    ]

if selected_work:
    filtered_df = filtered_df[
        filtered_df["work_mode"].isin(selected_work)
    ]

# ---------------------------------------
# Empty Data Check
# ---------------------------------------

if filtered_df.empty:

    st.warning(
        "⚠️ No jobs match the selected filters."
    )

    st.stop()

# ---------------------------------------
# KPI Cards
# ---------------------------------------

avg_salary = filtered_df["salary_midpoint_lpa"].mean()

median_salary = filtered_df["salary_midpoint_lpa"].median()

highest_salary = filtered_df["salary_midpoint_lpa"].max()

lowest_salary = filtered_df["salary_midpoint_lpa"].min()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Average Salary",
    f"{avg_salary:.2f} LPA"
)

col2.metric(
    "📊 Median Salary",
    f"{median_salary:.2f} LPA"
)

col3.metric(
    "📈 Highest Salary",
    f"{highest_salary:.2f} LPA"
)

col4.metric(
    "📉 Lowest Salary",
    f"{lowest_salary:.2f} LPA"
)

st.info(
    f"📌 Analysis based on **{len(filtered_df)}** disclosed salary jobs out of **{len(df)}** total jobs."
)

st.markdown("---")
# ---------------------------------------
# Common Data for Tabs
# ---------------------------------------

city_salary = (
    filtered_df
    .groupby("primary_city")["salary_midpoint_lpa"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

company_salary = (
    filtered_df
    .groupby("company_name")["salary_midpoint_lpa"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Distribution",
        "🏙 Cities",
        "🏢 Companies",
        "💡 Insights"
    ]
)
# ============================================
# TAB 1 : SALARY DISTRIBUTION
# ============================================

with tab1:

    st.subheader("📊 Salary Distribution")

    fig = px.histogram(
        filtered_df,
        x="salary_midpoint_lpa",
        nbins=25,
        color="salary_tier",
        template="plotly_white",
        title="Distribution of Disclosed Salaries"
    )

    fig.update_layout(
        xaxis_title="Salary (LPA)",
        yaxis_title="Number of Jobs"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("📦 Salary Spread")

    fig = px.box(
        filtered_df,
        y="salary_midpoint_lpa",
        color="salary_tier",
        template="plotly_white"
    )

    fig.update_layout(
        yaxis_title="Salary (LPA)"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

st.subheader("📈 Average Salary by Experience")

experience_salary = (
    filtered_df
    .groupby("experience_tier", as_index=False)["salary_midpoint_lpa"]
    .mean()
)

# Order experience levels
order = [
    "Fresher",
    "Junior (0-2 Yrs)",
    "Mid (3-5 Yrs)",
    "Senior (6-8 Yrs)",
    "Lead/Architect (9+ Yrs)"
]

experience_salary["experience_tier"] = pd.Categorical(
    experience_salary["experience_tier"],
    categories=order,
    ordered=True
)

experience_salary = experience_salary.sort_values("experience_tier")

fig = px.line(
    experience_salary,
    x="experience_tier",
    y="salary_midpoint_lpa",
    markers=True,
    title="Average Salary by Experience Level",
    template="plotly_white"
)

fig.update_layout(
    xaxis_title="Experience",
    yaxis_title="Average Salary (LPA)"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("🥧 Salary Tier Distribution")

tier_count = (
    filtered_df["salary_tier"]
    .value_counts()
    .reset_index()
)

tier_count.columns = ["Salary Tier", "Jobs"]

fig = px.pie(
    tier_count,
    values="Jobs",
    names="Salary Tier",
    hole=0.45,
    title="Salary Tier Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2 : CITY ANALYSIS
# ============================================

with tab2:

    st.subheader("🏙 Highest Paying Cities")

    # city_salary = (
    #     filtered_df
    #     .groupby("primary_city")["salary_midpoint_lpa"]
    #     .mean()
    #     .sort_values(ascending=False)
    #     .head(10)
    #     .reset_index()
    # )

    if city_salary.empty:

        st.warning("No city data available.")

    else:

        fig = px.bar(
            city_salary,
            x="salary_midpoint_lpa",
            y="primary_city",
            orientation="h",
            color="salary_midpoint_lpa",
            template="plotly_white",
            title="Top 10 Highest Paying Cities"
        )

        fig.update_layout(
            xaxis_title="Average Salary (LPA)",
            yaxis_title="City",
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success(
            f"""
🏆 Highest Paying City

**{city_salary.iloc[0]['primary_city']}**

Average Salary: **{city_salary.iloc[0]['salary_midpoint_lpa']:.2f} LPA**
"""
        )

    st.markdown("---")

    st.subheader("📍 Number of Jobs by City")

    city_jobs = (
        filtered_df["primary_city"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    city_jobs.columns = ["City", "Jobs"]

    fig = px.bar(
        city_jobs,
        x="Jobs",
        y="City",
        orientation="h",
        color="Jobs",
        template="plotly_white",
        title="Top Cities by Job Count"
    )

    st.plotly_chart(fig, use_container_width=True)
   # ============================================
# TAB 3 : COMPANY ANALYSIS
# ============================================

with tab3:

    st.subheader("🏢 Company Salary Analysis")

    if company_salary.empty:

        st.warning("⚠️ No company data available for the selected filters.")

    else:

        fig = px.bar(
            company_salary,
            x="salary_midpoint_lpa",
            y="company_name",
            orientation="h",
            color="salary_midpoint_lpa",
            template="plotly_white",
            text="salary_midpoint_lpa",
            title="Top 10 Highest Paying Companies"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Average Salary (LPA)",
            yaxis_title="Company",
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success(
            f"""
🏆 Highest Paying Company

**{company_salary.iloc[0]['company_name']}**

Average Salary: **{company_salary.iloc[0]['salary_midpoint_lpa']:.2f} LPA**
"""
        )

    st.markdown("---")

    st.subheader("🏢 Companies with Most Job Openings")

    company_jobs = (
        filtered_df["company_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    company_jobs.columns = ["Company", "Jobs"]

    fig2 = px.bar(
        company_jobs,
        x="Jobs",
        y="Company",
        orientation="h",
        color="Jobs",
        template="plotly_white",
        text="Jobs",
        title="Top Companies by Number of Job Openings"
    )

    fig2.update_traces(textposition="outside")

    fig2.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
        height=600
    )

    st.plotly_chart(fig2, use_container_width=True)
with tab4:

    st.subheader("💡 Salary Insights")

    c1, c2 = st.columns(2)

    with c1:

        if not city_salary.empty:
            st.success(
                f"🏙 Highest Paying City\n\n**{city_salary.iloc[0]['primary_city']}**"
            )

        if not company_salary.empty:
            st.success(
                f"🏢 Highest Paying Company\n\n**{company_salary.iloc[0]['company_name']}**"
            )

        st.success(
            f"💰 Average Salary\n\n**{avg_salary:.2f} LPA**"
        )

    with c2:

        st.info(
            f"📊 Median Salary\n\n**{median_salary:.2f} LPA**"
        )

        st.info(
            f"👨‍💻 Most Common Experience\n\n**{filtered_df['experience_tier'].mode()[0]}**"
        )

        st.info(
            f"💵 Most Common Salary Tier\n\n**{filtered_df['salary_tier'].mode()[0]}**"
        )

    st.markdown("---")

    st.subheader("📌 Dataset Summary")

    d1, d2, d3 = st.columns(3)

    d1.metric("Jobs", len(filtered_df))
    d2.metric("Companies", filtered_df["company_name"].nunique())
    d3.metric("Cities", filtered_df["primary_city"].nunique())

    st.markdown("---")

    st.subheader("📥 Download Filtered Dataset")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        "filtered_salary_data.csv",
        "text/csv"
    )

    st.markdown("---")

    st.subheader("🔍 Explore Jobs")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown("---")
st.subheader("🔍 Search Jobs")

search = st.text_input(
    "Search by Job Title or Company"
)

table = filtered_df.copy()

if search:

    table = table[
        table["job_title"].str.contains(search, case=False, na=False)
        |
        table["company_name"].str.contains(search, case=False, na=False)
    ]

st.dataframe(
    table[
        [
            "job_title",
            "company_name",
            "primary_city",
            "experience_tier",
            "salary_midpoint_lpa",
            "work_mode"
        ]
    ],
    use_container_width=True,
    hide_index=True
)