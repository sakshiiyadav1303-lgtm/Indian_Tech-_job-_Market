import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

st.set_page_config(
    page_title="Market Trends",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Trends")

st.markdown("Explore overall trends in the Indian Tech Job Market.")

st.markdown("---")

df = load_data()

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Remote Jobs",
    f"{(df['work_mode']=='Remote').sum():,}"
)

k2.metric(
    "Hybrid Jobs",
    f"{(df['work_mode']=='Hybrid').sum():,}"
)

k3.metric(
    "Freshers Friendly",
    f"{df['is_fresher_friendly'].sum():,}"
)

k4.metric(
    "Average Experience",
    f"{df['experience_min_yrs'].mean():.1f} yrs"
)

st.markdown("---")
# ==========================================
# MARKET DISTRIBUTION
# ==========================================

left, right = st.columns(2)

# ==========================================
# WORK MODE DISTRIBUTION
# ==========================================

with left:

    st.subheader("🏠 Work Mode Distribution")

    work_mode = (
        df["work_mode"]
        .value_counts()
        .reset_index()
    )

    work_mode.columns = ["Work Mode", "Jobs"]

    fig = px.pie(
        work_mode,
        names="Work Mode",
        values="Jobs",
        hole=0.45
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)


# ==========================================
# EXPERIENCE DISTRIBUTION
# ==========================================

with right:

    st.subheader("👨‍💻 Experience Distribution")

    exp = (
        df["experience_tier"]
        .value_counts()
        .reset_index()
    )

    exp.columns = ["Experience", "Jobs"]

    fig = px.bar(
        exp,
        x="Experience",
        y="Jobs",
        color="Jobs",
        text="Jobs",
        template="plotly_white"
    )

    fig.update_layout(
        height=500,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

left, right = st.columns(2)

# ==========================================
# SALARY TIER DISTRIBUTION
# ==========================================

with left:

    st.subheader("💰 Salary Tier Distribution")

    salary = (
        df["salary_tier"]
        .value_counts()
        .reset_index()
    )

    salary.columns = ["Salary Tier", "Jobs"]

    fig = px.bar(
        salary,
        x="Salary Tier",
        y="Jobs",
        color="Jobs",
        text="Jobs",
        template="plotly_white"
    )

    fig.update_layout(
        height=500,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
# ==========================================
# FRESHERS FRIENDLY
# ==========================================

with right:

    st.subheader("🎓 Freshers vs Experienced Jobs")

    fresher = pd.DataFrame({

        "Category": [
            "Freshers Friendly",
            "Experienced"
        ],

        "Jobs": [

            df["is_fresher_friendly"].sum(),

            len(df) - df["is_fresher_friendly"].sum()

        ]
    })

    fig = px.pie(
        fresher,
        names="Category",
        values="Jobs",
        hole=0.45
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("💡 Key Market Insights")

left, right = st.columns(2)

with left:

    st.success(
        f"""
🏠 Most Common Work Mode

**{df['work_mode'].mode()[0]}**
"""
    )

    st.success(
        f"""
👨‍💻 Most Common Experience

**{df['experience_tier'].mode()[0]}**
"""
    )

with right:

    st.info(
        f"""
💰 Most Common Salary Tier

**{df['salary_tier'].mode()[0]}**
"""
    )

    st.info(
        f"""
🎓 Freshers Friendly Jobs

**{df['is_fresher_friendly'].sum()}**
"""
    )
st.markdown("---")

st.download_button(
    "📥 Download Market Trends Data",
    df.to_csv(index=False),
    file_name="market_trends.csv",
    mime="text/csv"
)
st.markdown("---")

st.subheader("📋 Market Summary")

st.write(f"📄 Total Jobs : **{len(df)}**")

st.write(f"🏢 Companies : **{df['company_name'].nunique()}**")

st.write(f"📍 Cities : **{df['primary_city'].nunique()}**")

st.write(f"🧠 Skill Domains : **{df['skill_domain'].nunique()}**")

st.write(f"⭐ Average Company Rating : **{df['company_rating'].mean():.2f}**")

st.write(f"💰 Average Salary (Disclosed) : **{df['salary_midpoint_lpa'].mean():.2f} LPA**")