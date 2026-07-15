import streamlit as st

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="About",
    page_icon="📌",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("📌 About This Project")

st.markdown("""
Welcome to the **Indian Tech Job Market Analysis 2026** dashboard.

This project is an interactive data analytics dashboard built using **Python**, **Streamlit**, **Pandas**, and **Plotly**. It helps users explore salary trends, company insights, hiring locations, required skills, and overall market trends in the Indian technology industry.
""")

st.divider()

# ==========================================
# PROJECT OVERVIEW
# ==========================================

st.header("📖 Project Overview")

st.write("""
The objective of this project is to analyze the Indian Technology Job Market using interactive data visualizations.

The dashboard allows users to:

- Explore salary trends across companies and cities.
- Identify the most demanded technical skills.
- Analyze company hiring patterns.
- Compare company ratings and salaries.
- Study market trends.
- Search jobs using interactive filters.

This project demonstrates practical implementation of **Data Cleaning**, **Exploratory Data Analysis (EDA)**, **Business Intelligence**, and **Interactive Dashboard Development**.
""")

st.divider()

# ==========================================
# PROJECT OBJECTIVES
# ==========================================

st.header("🎯 Project Objectives")

col1, col2 = st.columns(2)

with col1:
    st.success("""
- Analyze the Indian Tech Job Market
- Study salary trends
- Identify in-demand skills
- Explore company hiring
""")

with col2:
    st.info("""
- Compare company ratings
- Analyze hiring locations
- Visualize market trends
- Build an interactive dashboard
""")

st.divider()
# ==========================================
# DASHBOARD FEATURES
# ==========================================

st.header("📊 Dashboard Features")

col1, col2 = st.columns(2)

with col1:

    st.success("""
### Available Dashboard Pages

🏠 Home Dashboard

💰 Salary Analysis

🧠 Skills Analysis

🏢 Company Insights
""")

with col2:

    st.info("""
### More Dashboard Pages

📍 Location Analysis

📈 Market Trends

🔍 Job Explorer

📌 About
""")

st.divider()

# ==========================================
# TECHNOLOGIES USED
# ==========================================

st.header("🛠 Technologies Used")

c1, c2, c3 = st.columns(3)

c1.metric("🐍 Language", "Python")

c2.metric("🎈 Framework", "Streamlit")

c3.metric("📊 Visualization", "Plotly")

c4, c5, c6 = st.columns(3)

c4.metric("🐼 Data Analysis", "Pandas")

c5.metric("🔢 Numerical", "NumPy")

c6.metric("📄 Excel Support", "OpenPyXL")

st.divider()

# ==========================================
# DATASET INFORMATION
# ==========================================

st.header("📂 Dataset Information")

st.write("""
The dataset used in this project contains information related to the Indian Technology Job Market.

### Dataset includes:

- Job Title
- Company Name
- Company Rating
- Company Size
- City
- Experience Level
- Salary Information
- Salary Tier
- Skills Required
- Skill Domain
- Work Mode

### Data Preparation

Before building the dashboard, the dataset was:

✅ Cleaned

✅ Missing values handled

✅ Duplicate records removed

✅ Salary tiers created

✅ Experience categories standardized

✅ Skill domains organized

This preprocessing helped improve the quality and reliability of the analysis.
""")

st.divider()
# ==========================================
# PROJECT STATISTICS
# ==========================================

st.header("📈 Project Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📄 Dashboard Pages",
    "8"
)

col2.metric(
    "📊 Interactive Charts",
    "20+"
)

col3.metric(
    "🎯 Filters",
    "15+"
)

col4.metric(
    "🛠 Technologies",
    "6"
)

st.divider()

# ==========================================
# FUTURE SCOPE
# ==========================================

st.header("🚀 Future Scope")

left, right = st.columns(2)

with left:

    st.success("""
### Planned Improvements

- AI Salary Prediction

- Resume Matching

- Live Job API Integration

- Company Comparison Dashboard

- Job Recommendation System
""")

with right:

    st.info("""
### Advanced Features

- Skill Gap Analysis

- Career Recommendation

- Interactive Maps

- Real-time Analytics

- Mobile Friendly Dashboard
""")

st.divider()

# ==========================================
# DEVELOPER
# ==========================================

st.header("👨‍💻 Developer")

st.markdown("""
### **Sakshi**

**Project:** Indian Tech Job Market Analysis 2026

This project was developed as part of a Data Analytics learning journey to demonstrate practical skills in:

- Python Programming
- Data Cleaning
- Exploratory Data Analysis (EDA)
- Interactive Dashboard Development
- Business Intelligence
- Data Visualization
""")

st.divider()

# ==========================================
# ACKNOWLEDGEMENT
# ==========================================

st.header("🙏 Acknowledgement")

st.write("""
I would like to express my gratitude to everyone who contributed directly or indirectly to the successful completion of this project.

Special thanks to the open-source Python community and the developers of **Streamlit**, **Pandas**, and **Plotly** for providing powerful tools that made this dashboard possible.

This project was created for educational purposes to enhance practical knowledge in Data Analytics and Dashboard Development.
""")

st.divider()

# ==========================================
# THANK YOU
# ==========================================

st.success("🎉 Thank you for exploring the Indian Tech Job Market Analysis Dashboard!")

st.caption("Developed using ❤️ Python • Streamlit • Pandas • Plotly")