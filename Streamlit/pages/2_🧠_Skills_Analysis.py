import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Skills Analysis",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Skills Analysis Dashboard")

st.markdown(
    "Discover the most in-demand skills in the Indian Technology Job Market."
)
st.markdown("---")

# ---------------------------------------
# Load Dataset
# ---------------------------------------

df = load_data()

# ---------------------------------------
# Create One Row Per Skill
# ---------------------------------------

skills = (
    df.assign(
        skill=df["skills_required"].str.split(",")
    )
    .explode("skill")
)

# Clean skill names
skills["skill"] = (
    skills["skill"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
)

# Remove empty skills
skills = skills[
    skills["skill"] != ""
]

# Standardize common skill names
skill_mapping = {

    # Python
    "python": "Python",
    "python3": "Python",
    "python programming": "Python",

    # SQL
    "sql": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    "sql server": "SQL",

    # Machine Learning
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",

    # Artificial Intelligence
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",

    # Deep Learning
    "deep learning": "Deep Learning",

    # Data Analysis
    "analytics": "Data Analysis",
    "analytical": "Data Analysis",
    "analysis": "Data Analysis",
    "analysing": "Data Analysis",
    "analyzing": "Data Analysis",
    "data": "Data Analysis",
    "data analysis": "Data Analysis",

    # Data Engineering
    "data engineering": "Data Engineering",

    # Business Analysis
    "business analysis": "Business Analysis",
    "business analyst": "Business Analysis",

    # Visualization
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "tableau": "Tableau",

    # Cloud
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",

    # Excel
    "excel": "Excel",
    "ms excel": "Excel",
    "microsoft excel": "Excel",

    # Programming
    "java": "Java",
    "javascript": "JavaScript",
    "c++": "C++",
    "c#": "C#",
    "html": "HTML",
    "css": "CSS",

    # Version Control
    "git": "Git",
    "github": "GitHub",

    # Soft Skills
    "communication": "Communication",
    "problem solving": "Problem Solving",
    "leadership": "Leadership",
    "teamwork": "Teamwork",

    # Other
    "agile": "Agile",
    "automation": "Automation",
    "computer science": "Computer Science"
}

skills["skill"] = skills["skill"].replace(skill_mapping)

# Convert remaining skills to Title Case
skills["skill"] = skills["skill"].apply(
    lambda x: skill_mapping.get(x.lower(), x.title())
)
# ---------------------------------------
# Sidebar Filters
# ---------------------------------------

st.sidebar.header("🎯 Filters")

cities = sorted(df["primary_city"].dropna().unique())

work_modes = sorted(df["work_mode"].dropna().unique())

experience = sorted(df["experience_tier"].dropna().unique())

selected_city = st.sidebar.multiselect(
    "📍 City",
    cities
)

selected_work = st.sidebar.multiselect(
    "🏠 Work Mode",
    work_modes
)

selected_exp = st.sidebar.multiselect(
    "👨‍💻 Experience",
    experience
)

filtered = skills.copy()

if selected_city:
    filtered = filtered[
        filtered["primary_city"].isin(selected_city)
    ]

if selected_work:
    filtered = filtered[
        filtered["work_mode"].isin(selected_work)
    ]

if selected_exp:
    filtered = filtered[
        filtered["experience_tier"].isin(selected_exp)
    ]

if filtered.empty:

    st.warning("No data found.")

    st.stop()
# ---------------------------------------
# KPI Cards
# ---------------------------------------

skill_count = (
    filtered["skill"]
    .value_counts()
)

top_skill = skill_count.index[0]

total_skills = filtered["skill"].nunique()

avg_skills = (
    filtered.groupby("job_id")["skill"]
    .count()
    .mean()
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "🔥 Top Skill",
    top_skill
)

col2.metric(
    "🧠 Unique Skills",
    total_skills
)

col3.metric(
    "📊 Avg Skills / Job",
    f"{avg_skills:.1f}"
)

st.markdown("---")
st.subheader("🔥 Top 20 Most Demanded Skills")

top_skills = (
    filtered["skill"]
    .value_counts()
    .head(20)
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
    template="plotly_white",
    title="Top 20 Most Demanded Skills"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    height=700,
    yaxis=dict(categoryorder="total ascending"),
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("📊 Skill Domain Distribution")

domain = (
    filtered["skill_domain"]
    .value_counts()
    .reset_index()
)

domain.columns = ["Domain", "Jobs"]

fig = px.pie(
    domain,
    names="Domain",
    values="Jobs",
    hole=0.45,
    title="Skills by Domain"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("📋 Top Skills Table")

st.dataframe(
    top_skills,
    use_container_width=True,
    hide_index=True
)
st.markdown("---")

st.subheader("🔍 Search a Skill")

search_skill = st.text_input(
    "Enter a skill (Example: Python, SQL, AWS)"
)

if search_skill:

    skill_df = filtered[
        filtered["skill"]
        .str.contains(search_skill, case=False, na=False)
    ]

    st.write(f"### Jobs requiring **{search_skill}**")

    st.metric(
        "Jobs Found",
        len(skill_df)
    )

    st.dataframe(
        skill_df[
            [
                "job_title",
                "company_name",
                "primary_city",
                "experience_tier",
                "salary_midpoint_lpa"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )