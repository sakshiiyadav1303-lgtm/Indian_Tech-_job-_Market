import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="Indian Tech Job Market Analysis 2026",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

@st.cache_data
def load_data():
    # Resolves path dynamically to fix the FileNotFoundError on Streamlit Cloud
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "Data", "indian_tech_jobs_cleaned.csv")
    
    # Fallback configuration if root structure shifts
    if not os.path.exists(data_path):
        data_path = os.path.join(current_dir, "Data", "indian_tech_jobs_cleaned.csv")
        
    return pd.read_csv(data_path)

df = load_data()

# ---------------------------------------
# SIDEBAR FILTER
# ---------------------------------------

st.sidebar.header("🎯 Dashboard Filter")

city = st.sidebar.selectbox(
    "📍 Select City",
    ["All"] + sorted(df["primary_city"].dropna().unique())
)

filtered_df = df.copy()

if city != "All":
    filtered_df = filtered_df[
        filtered_df["primary_city"] == city
    ]

# ---------------------------------------
# TITLE
# ---------------------------------------

st.title("📊 Indian Tech Job Market Analysis 2026")

st.markdown("---")

# ---------------------------------------
# ABOUT PROJECT
# ---------------------------------------

st.subheader("📖 About This Project")

st.write("""
This dashboard analyzes the **Indian Technology Job Market** using
**Python, Pandas, Plotly and Streamlit**.

The dashboard provides insights into:

- 💰 Salary Analysis
- 🧠 Skills Analysis
- 🏢 Company Insights
- 📍 Location Analysis
- 📈 Market Trends
- 🔍 Interactive Job Explorer

Use the pages in the left sidebar to explore each analysis in detail.
""")

st.markdown("---")

# ============================================
# DASHBOARD OVERVIEW (KPIs)
# ============================================

st.subheader("📊 Dashboard Overview")

salary_df = filtered_df[
    (filtered_df["salary_disclosed"] == True)
    &
    (filtered_df["salary_midpoint_lpa"].notna())
].copy()

total_jobs = len(filtered_df)
total_companies = filtered_df["company_name"].nunique()
total_cities = filtered_df["primary_city"].nunique()
avg_salary = salary_df["salary_midpoint_lpa"].mean()
avg_rating = filtered_df["company_rating"].mean()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("📄 Total Jobs", f"{total_jobs:,}")
k2.metric("🏢 Companies", total_companies)
k3.metric("📍 Cities", total_cities)
k4.metric("💰 Avg Salary", f"{avg_salary:.2f} LPA")
k5.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

st.markdown("---")

# ============================================
# QUICK INSIGHTS
# ============================================

st.subheader("⚡ Quick Insights")

# Highest Paying City
city_salary = (
    salary_df
    .groupby("primary_city")["salary_midpoint_lpa"]
    .mean()
)
highest_city = city_salary.idxmax() if not city_salary.empty else "N/A"

# Highest Paying Company
company_salary = (
    salary_df
    .groupby("company_name")["salary_midpoint_lpa"]
    .mean()
)
highest_company = company_salary.idxmax() if not company_salary.empty else "N/A"

# Most Demanded Skill
skills = (
    filtered_df["skills_required"]
    .fillna("")
    .str.split(",")
    .explode()
    .str.strip()
)
skills = skills[skills != ""]
top_skill = skills.value_counts().idxmax() if not skills.empty else "N/A"

# Most Hiring City
top_hiring_city = (
    filtered_df["primary_city"]
    .value_counts()
    .idxmax()
)

c1, c2 = st.columns(2)

with c1:
    st.success(f"""
🏙 **Highest Paying City**

**{highest_city}**
""")

    st.success(f"""
🏢 **Highest Paying Company**

**{highest_company}**
""")

with c2:
    st.info(f"""
🔥 **Most Demanded Skill**

**{top_skill}**
""")

    st.info(f"""
📍 **Most Hiring City**

**{top_hiring_city}**
""")

st.markdown("---")

# ============================================
# CHARTS SECTION
# ============================================

left, right = st.columns(2)

# ==========================
# LEFT COLUMN
# ==========================
with left:
    st.subheader("📍 Top Hiring Cities")

    city_jobs = (
        filtered_df["primary_city"]
        .fillna("Unknown")
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
        text="Jobs",
        template="plotly_white"
    )

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# RIGHT COLUMN
# ==========================
with right:
    st.subheader("🧠 Top Skills")

    skills = (
        filtered_df["skills_required"]
        .fillna("")
        .str.split(",")
        .explode()
        .str.strip()
    )
    skills = skills[skills != ""]

    top_skills = (
        skills
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_skills.columns = ["Skill", "Jobs"]

    fig = px.bar(
        top_skills,
        x="Jobs",
        y="Skill",
        orientation="h",
        color="Jobs",
        text="Jobs",
        template="plotly_white"
    )

    fig.update_layout(
        height=500,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# SALARY OVERVIEW
# ============================================

st.subheader("💰 Salary Overview")

salary_df = filtered_df[
    (filtered_df["salary_disclosed"] == True)
    &
    (filtered_df["salary_midpoint_lpa"].notna())
]

avg_salary = salary_df["salary_midpoint_lpa"].mean()
median_salary = salary_df["salary_midpoint_lpa"].median()
highest_salary = salary_df["salary_midpoint_lpa"].max()
lowest_salary = salary_df["salary_midpoint_lpa"].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Salary", f"{avg_salary:.2f} LPA")
c2.metric("Median Salary", f"{median_salary:.2f} LPA")
c3.metric("Highest Salary", f"{highest_salary:.2f} LPA")
c4.metric("Lowest Salary", f"{lowest_salary:.2f} LPA")

fig = px.histogram(
    salary_df,
    x="salary_midpoint_lpa",
    nbins=25,
    color="salary_tier",
    template="plotly_white",
    title="Salary Distribution (Disclosed Salaries Only)"
)

fig.update_layout(
    xaxis_title="Salary (LPA)",
    yaxis_title="Jobs",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.info(f"""
📌 Salary Analysis is based on **{len(salary_df)}** disclosed salaries
out of **{len(filtered_df)}** total jobs.
""")

st.markdown("---")

# ============================================
# DASHBOARD FEATURES & SUMMARY
# ============================================

st.subheader("✨ Dashboard Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
### 📊 Analytics
✅ Salary Analysis
✅ Skills Analysis
✅ Company Analysis
✅ Location Analysis
""")

with col2:
    st.markdown("""
### 🎯 Interactive
✅ Sidebar Filters
✅ Plotly Charts
✅ KPI Cards
✅ Search & Exploration
""")

with col3:
    st.markdown("""
### 📈 Insights
✅ Salary Trends
✅ Hiring Trends
✅ Skills Demand
✅ Work Mode Analysis
""")

st.info(f"""
**Dataset Summary**

📄 Total Jobs : **{len(filtered_df)}**
🏢 Companies : **{filtered_df['company_name'].nunique()}**
📍 Cities : **{filtered_df['primary_city'].nunique()}**
🧠 Skill Domains : **{filtered_df['skill_domain'].nunique()}**
""")

st.markdown("---")

# ============================================
# FOOTER
# ============================================

st.markdown(
    """
    <center>
    <h1>📊 Indian Tech Job Market Dashboard</h1>
    <h3>Built using</h3>
    <p>🐍 Python • 🐼 Pandas • 📈 Plotly • ⚡ Streamlit</p>
    <hr>
    <p>Created as a <strong>Data Analytics Portfolio Project</strong></p>
    </center>
    """,
    unsafe_allow_html=True
)