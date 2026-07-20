import streamlit as st
import pandas as pd

from utils import load_data

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Job Explorer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Job Explorer")

st.markdown("""
Search and explore jobs from the Indian Tech Job Market.
""")

st.markdown("---")

# =====================================
# LOAD DATA
# =====================================

df = load_data()

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.header("🎯 Filters")

city = st.sidebar.multiselect(
    "📍 City",
    sorted(df["primary_city"].dropna().unique())
)

experience = st.sidebar.multiselect(
    "👨‍💻 Experience",
    sorted(df["experience_tier"].dropna().unique())
)

work_mode = st.sidebar.multiselect(
    "🏠 Work Mode",
    sorted(df["work_mode"].dropna().unique())
)

salary = st.sidebar.multiselect(
    "💰 Salary Tier",
    sorted(df["salary_tier"].dropna().unique())
)

search = st.text_input(
    "🔎 Search Job Title or Company"
)

filtered_df = df.copy()

if city:
    filtered_df = filtered_df[
        filtered_df["primary_city"].isin(city)
    ]

if experience:
    filtered_df = filtered_df[
        filtered_df["experience_tier"].isin(experience)
    ]

if work_mode:
    filtered_df = filtered_df[
        filtered_df["work_mode"].isin(work_mode)
    ]

if salary:
    filtered_df = filtered_df[
        filtered_df["salary_tier"].isin(salary)
    ]

if search:

    filtered_df = filtered_df[
        filtered_df["job_title"]
        .str.contains(search, case=False, na=False)

        |

        filtered_df["company_name"]
        .str.contains(search, case=False, na=False)
    ]

if filtered_df.empty:

    st.warning("⚠ No jobs found.")

    st.stop()
st.markdown("---")

st.subheader("📊 Search Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Jobs",
    len(filtered_df)
)

c2.metric(
    "Companies",
    filtered_df["company_name"].nunique()
)

c3.metric(
    "Cities",
    filtered_df["primary_city"].nunique()
)

c4.metric(
    "Skills",
    filtered_df["skill_domain"].nunique()
)

st.markdown("---")
st.subheader("📄 Job Listings")

columns = [
    "job_title",
    "company_name",
    "primary_city",
    "experience_tier",
    "salary_tier",
    "work_mode",
    "salary_midpoint_lpa",
    "company_rating"
]

st.dataframe(
    filtered_df[columns],
    use_container_width=True,
    hide_index=True
)
st.markdown("---")

st.download_button(
    "📥 Download Filtered Jobs",
    filtered_df.to_csv(index=False),
    "filtered_jobs.csv",
    "text/csv"
)