import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Company Insights",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Company Insights")
st.markdown("Analyze hiring companies, ratings and salary trends.")
st.markdown("---")

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

# Data for ALL company analysis
company_df = df.copy()

# Data ONLY for salary analysis
salary_df = df[
    (df["salary_disclosed"] == True) &
    (df["salary_midpoint_lpa"].notna())
].copy()

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🎯 Filters")

selected_size = st.sidebar.multiselect(
    "Company Size",
    sorted(company_df["company_size_bucket"].dropna().unique())
)

selected_rating = st.sidebar.slider(
    "Minimum Company Rating",
    0.0,
    5.0,
    0.0,
    0.1
)

# Apply filters

if selected_size:

    company_df = company_df[
        company_df["company_size_bucket"].isin(selected_size)
    ]

    salary_df = salary_df[
        salary_df["company_size_bucket"].isin(selected_size)
    ]

company_df = company_df[
    company_df["company_rating"] >= selected_rating
]

salary_df = salary_df[
    salary_df["company_rating"] >= selected_rating
]

if company_df.empty:

    st.warning("⚠ No companies found.")

    st.stop()

# ==========================================
# KPI CARDS
# ==========================================

total_companies = company_df["company_name"].nunique()

avg_rating = company_df["company_rating"].mean()

most_hiring = (
    company_df["company_name"]
    .value_counts()
    .idxmax()
)

highest_paying = (
    salary_df
    .groupby("company_name")["salary_midpoint_lpa"]
    .mean()
    .idxmax()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏢 Companies", total_companies)
c2.metric("⭐ Avg Rating", f"{avg_rating:.2f}")
c3.metric("🔥 Most Hiring", most_hiring)
c4.metric("💰 Highest Paying", highest_paying)

st.markdown("---")
# ==========================================
# TOP HIRING vs HIGHEST PAYING
# ==========================================

left, right = st.columns(2)

# ==========================================
# TOP HIRING COMPANIES
# ==========================================

with left:

    st.subheader("🔥 Top Hiring Companies")

    hiring = (
        company_df["company_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    hiring.columns = ["Company", "Jobs"]

    fig = px.bar(
        hiring,
        x="Jobs",
        y="Company",
        orientation="h",
        color="Jobs",
        text="Jobs",
        template="plotly_white",
        color_continuous_scale="Blues"
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# HIGHEST PAYING COMPANIES
# ==========================================

with right:

    st.subheader("💰 Highest Paying Companies")

    paying = (
        salary_df
        .groupby("company_name")["salary_midpoint_lpa"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    paying.columns = ["Company", "Average Salary"]

    fig = px.bar(
        paying,
        x="Average Salary",
        y="Company",
        orientation="h",
        color="Average Salary",
        text="Average Salary",
        template="plotly_white",
        color_continuous_scale="Greens"
    )

    fig.update_traces(
        texttemplate="%{text:.1f} LPA",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# HIGHEST RATED COMPANIES
# ==========================================

with left:

    st.subheader("⭐ Highest Rated Companies")

    rated = (
        company_df
        .groupby("company_name")
        .agg(
            Rating=("company_rating", "mean"),
            Jobs=("company_name", "count")
        )
        .reset_index()
    )

    # Keep companies with at least 2 job postings
    rated = rated[rated["Jobs"] >= 2]

    rated = rated.sort_values(
        "Rating",
        ascending=False
    ).head(10)

    fig = px.bar(
        rated,
        x="Rating",
        y="company_name",
        orientation="h",
        color="Rating",
        text="Rating",
        template="plotly_white",
        color_continuous_scale="Purples"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="highest_rated_chart"
    )

# ==========================================
# COMPANY SIZE DISTRIBUTION
# ==========================================

with right:

    st.subheader("🏭 Company Size Distribution")

    size = (
        company_df["company_size_bucket"]
        .value_counts()
        .reset_index()
    )

    size.columns = ["Company Size", "Count"]

    fig = px.pie(
        size,
        names="Company Size",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="company_size_chart"
    )
rated = (
    company_df
    .groupby("company_name")
    .agg(
        Rating=("company_rating", "mean"),
        Jobs=("company_name", "count")
    )
    .reset_index()
)

rated = rated[
    rated["Jobs"] >= 2
]

rated = rated.sort_values(
    "Rating",
    ascending=False
).head(10)

# ==========================================
# COMPANY INSIGHTS
# ==========================================

st.subheader("💡 Company Insights")
col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
🏆 Highest Paying Company

**{paying.iloc[0]['Company']}**

Average Salary

**{paying.iloc[0]['Average Salary']:.2f} LPA**
"""
    )

    st.success(
        f"""
🔥 Most Hiring Company

**{hiring.iloc[0]['Company']}**

Jobs Posted

**{hiring.iloc[0]['Jobs']}**
"""
    )

with col2:

    st.info(
        f"""
⭐ Highest Rated Company

**{rated.iloc[0]['company_name']}**

Rating

**{rated.iloc[0]['Rating']:.2f}**
"""
    )

    st.info(
        f"""
🏭 Most Common Company Size

**{company_df['company_size_bucket'].mode()[0]}**
"""
    )
st.markdown("---")

st.subheader("📥 Download Company Data")

st.download_button(
    label="Download Company Insights Data",
    data=company_df.to_csv(index=False),
    file_name="company_insights.csv",
    mime="text/csv"
)
st.markdown("---")

st.subheader("📊 Company Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Companies",
    company_df["company_name"].nunique()
)

col2.metric(
    "Average Rating",
    f"{company_df['company_rating'].mean():.2f}"
)

col3.metric(
    "Average Salary",
    f"{salary_df['salary_midpoint_lpa'].mean():.2f} LPA"
)
st.markdown("---")

summary = pd.DataFrame({

    "Metric": [
        "Companies",
        "Jobs",
        "Average Rating",
        "Highest Salary",
        "Lowest Salary",
        "Most Hiring Company"
    ],

    "Value": [

        company_df["company_name"].nunique(),

        len(company_df),

        round(company_df["company_rating"].mean(), 2),

        round(salary_df["salary_midpoint_lpa"].max(), 2),

        round(salary_df["salary_midpoint_lpa"].min(), 2),

        hiring.iloc[0]["Company"]

    ]

})

st.subheader("📋 Dataset Summary")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)