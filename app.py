import os
import datetime
import extra_streamlit_components as stx
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

from backend import get_backend, show_authentication, logout_button

# Safe import for Gemini SDK
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="My Engineering Degree OS",
    page_icon="❤️‍🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
today_dt = pd.Timestamp(datetime.date.today())


# =========================================================
# MODERN ACADEMIC OS — LIGHT + FUTURISTIC DESIGN
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ink: #252B49;
        --muted: #8189A2;
        --purple: #686DDA;
        --purple-soft: #F0F0FF;
        --blue: #55A8D7;
        --mint: #37B99A;
        --coral: #F08B79;
        --amber: #E6A942;
        --line: #E9ECF5;
        --surface: #FFFFFF;
        --page: #F6F7FC;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 5% 0%, rgba(190, 184, 255, .18), transparent 28%),
            radial-gradient(ellipse at 95% 8%, rgba(139, 218, 220, .15), transparent 25%),
            var(--page);
        color: var(--ink);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--ink) !important;
        letter-spacing: -0.6px;
    }

    h1 {
        font-weight: 800 !important;
        letter-spacing: -1.2px;
    }

    h2, h3 {
        font-weight: 700 !important;
    }

    p, label, .stCaption {
        color: #69718A;
    }

    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.6rem;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 7px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: #F7F8FC;
        border: 1px solid transparent;
        border-radius: 12px;
        padding: 9px 12px;
        transition: all .18s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: #F0F1FF;
        border-color: #E2E4FF;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(100deg, #EFEEFF, #F5F8FF);
        border: 1px solid #DCDDFB;
        box-shadow: inset 3px 0 0 #777CEB;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #FFFFFF 55%, #F7F6FF);
        border: 1px solid #E7E8F6;
        border-radius: 19px;
        padding: 18px 19px 15px;
        box-shadow: 0 7px 22px rgba(50, 55, 110, .055);
        min-height: 122px;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #FFFFFF 52%, #F0EEFF);
        border-color: #E4E0FF;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #FFFFFF 52%, #EAF7FF);
        border-color: #DCEEF9;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #FFFFFF 52%, #EAF9F3);
        border-color: #D9F0E6;
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #FFFFFF 52%, #FFF2EC);
        border-color: #F7E4DA;
    }

    div[data-testid="stMetricLabel"] {
        color: #8189A2 !important;
        font-size: .83rem !important;
        font-weight: 650 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #343B70 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetricDelta"] {
        font-weight: 650 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, .92);
        border: 1px solid rgba(226, 230, 244, .95);
        border-radius: 20px;
        box-shadow: 0 7px 24px rgba(35, 48, 90, .045);
        transition: box-shadow .2s ease, transform .2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 10px 28px rgba(65, 73, 145, .075);
    }

    .stButton > button {
        border-radius: 11px;
        border: 1px solid #E1E5F2;
        background: #FFFFFF;
        color: #46517D;
        font-weight: 650;
        padding: .55rem 1rem;
        transition: all .18s ease;
    }

    .stButton > button:hover {
        border-color: #AEB3F2;
        background: #F0F1FF;
        color: #5057BE;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #7377E5, #5B9FD2);
        color: #FFFFFF;
        border: 1px solid transparent;
        box-shadow: 0 5px 13px rgba(104, 109, 218, .18);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(110deg, #6267D4, #4C8FC4);
        border-color: transparent;
        color: #FFFFFF;
        box-shadow: 0 7px 17px rgba(104, 109, 218, .25);
    }

    .stTextInput input, .stTextArea textarea, .stDateInput input {
        border-radius: 11px !important;
        border-color: #E1E5F0 !important;
        background: #FFFFFF !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        overflow: hidden;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #777CEB 0%, #61B6D6 55%, #56C5A3 100%);
        border-radius: 20px;
    }

    .stProgress > div > div {
        background: #E9ECF7;
        border-radius: 20px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--line);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        color: #777F99;
        font-weight: 650;
    }

    .stTabs [aria-selected="true"] {
        color: #6268D5 !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 13px;
    }

    hr {
        border-color: var(--line);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 23px 27px 24px;
        margin: 2px 0 22px 0;
        border: 1px solid rgba(222, 224, 250, .9);
        border-radius: 23px;
        background:
            radial-gradient(circle at 88% 15%, rgba(255,255,255,.9), transparent 20%),
            linear-gradient(112deg, #F0EEFF 0%, #F2F7FF 48%, #EAF9F5 100%);
        box-shadow: 0 9px 25px rgba(75, 81, 150, .055);
    }

    .hero:after {
        content: "❤️‍🔥";
        position: absolute;
        right: 7%;
        top: 8px;
        color: rgba(112, 117, 218, .17);
        font-size: 88px;
        line-height: 1;
        pointer-events: none;
    }

    .eyebrow {
        color: #777CE0;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.7px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .hero-title {
        color: #252B49;
        font-size: clamp(27px, 3vw, 36px);
        line-height: 1.15;
        font-weight: 850;
        letter-spacing: -1.4px;
    }

    .hero-subtitle {
        color: #858CA3;
        font-size: 14px;
        margin-top: 8px;
    }

    .section-kicker {
        color: #777CE0;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .mini-card {
        background: #FFFFFF;
        border: 1px solid #E9ECF5;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 4px 16px rgba(35, 48, 90, .03);
        min-height: 105px;
    }

    .colour-strip {
        height: 5px;
        border-radius: 20px;
        margin: -2px 0 13px 0;
        background: linear-gradient(90deg, #8A82EA, #72B9D8, #68C8A8, #F2B77B);
    }

    .status-pill {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: .2px;
    }

    .mini-card-label {
        color: #858CA3;
        font-size: 12px;
        font-weight: 650;
        margin-bottom: 7px;
    }

    .mini-card-value {
        color: #343B70;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -.5px;
    }

    .mini-card-note {
        color: #9299AF;
        font-size: 11px;
        margin-top: 4px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        div[data-testid="stMetric"] {
            padding: 14px;
        }
        .hero {
            padding: 19px;
        }
        .hero:after {
            right: 3%;
            font-size: 62px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def page_header(kicker, title, subtitle, emoji=""):
    """Render a consistent page heading across the app."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{kicker}</div>
            <div class="hero-title">{emoji} {title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text):
    st.markdown(
        f'<div class="section-kicker">{text}</div>',
        unsafe_allow_html=True,
    )


def get_1d_series(df, col_name, fallback_val=""):
    """Safely return a one-dimensional Series for a column."""
    matching_cols = [
        c for c in df.columns
        if str(c).strip().lower() == str(col_name).strip().lower()
    ]
    if matching_cols:
        series_obj = df[matching_cols[0]]
        if isinstance(series_obj, pd.DataFrame):
            return series_obj.iloc[:, 0]
        return series_obj
    return pd.Series([fallback_val] * len(df), index=df.index)


def safe_date_string(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if pd.isna(value):
        return None
    return str(value)


# =========================================================
# DEFAULT DATASETS
# =========================================================
DEFAULT_SEMESTERS = pd.DataFrame({
    "Semester": [f"Semester {i}" for i in range(1, 9)],
    "Status": [
        "Completed", "Completed", "Completed", "In Progress",
        "Not Started", "Not Started", "Not Started", "Not Started",
    ],
    "Target Credits": [20, 20, 22, 22, 20, 20, 18, 16],
    "Completed Credits": [20, 20, 22, 10, 0, 0, 0, 0],
    "Focus Area": [
        "Foundational Sciences & Math",
        "Programming & Circuits",
        "Data Structures & OOP",
        "Algorithms & Databases",
        "Operating Systems & Networks",
        "Software Engineering & Web",
        "Electives & Minor Project",
        "Major Capstone & Internship",
    ],
})

DEFAULT_COURSES = pd.DataFrame({
    "Semester": [
        "Semester 1", "Semester 1", "Semester 2", "Semester 2",
        "Semester 3", "Semester 3", "Semester 4", "Semester 4",
    ],
    "Course Code": ["MA101", "PH101", "CS102", "EE101", "CS201", "EC202", "CS202", "CS203"],
    "Course Title": [
        "Engineering Mathematics I", "Engineering Physics", "Problem Solving & Python",
        "Basic Electrical Engineering", "Data Structures", "Digital Logic Design",
        "Design & Analysis of Algorithms", "Database Management Systems",
    ],
    "Credits": [4, 4, 4, 3, 4, 3, 4, 4],
    "Syllabus Topics": [
        "Calculus, Matrices, ODEs",
        "Optics, Quantum Mechanics, Lasers",
        "Control structures, functions, files, OOP basics",
        "AC/DC circuits, transformers, induction motors",
        "Arrays, Linked Lists, Stacks, Queues, Trees, Graphs",
        "Boolean algebra, Logic gates, Combinational circuits, FSM",
        "Sorting, Divide & Conquer, Greedy, DP, Graph algorithms",
        "ER models, SQL, Normalization, Transactions, Indexing",
    ],
    "Status": [
        "Completed", "Completed", "Completed", "Completed",
        "Completed", "In Progress", "In Progress", "Not Started",
    ],
})

DEFAULT_UNIV_SYLLABUS = pd.DataFrame({
    "Programme": ["Bachelor of Engineering in Computer Science"],
    "Total Semesters": [8],
    "Total Credits Required": [158],
    "Curriculum Version": ["2024-2028 CBCS Scheme"],
    "Syllabus Source / Reference": ["University Academic Council Curriculum Handbook v4.2"],
    "Program Overview": [
        "Comprehensive 4-year undergraduate curriculum focusing on core computing principles, hardware-software integration, algorithms, data engineering, and project-based learning."
    ],
})

DEFAULT_CALENDAR = pd.DataFrame({
    "Date": ["2026-11-05", "2026-11-09", "2026-11-14", "2026-11-25", "2026-12-10"],
    "Event Title": [
        "Semester Classes Resume",
        "Internal Assessment 1 (IA1)",
        "Diwali / Festive Holiday",
        "Internal Assessment 2 (IA2)",
        "End Semester Examinations",
    ],
    "Type": ["Academic", "Assessment", "Leave", "Assessment", "Exam"],
    "Academic Year": ["2026-2027"] * 5,
    "Semester": ["Semester 4"] * 5,
})

DEFAULT_ASSESSMENTS = pd.DataFrame({
    "Course Code": ["CS202", "CS202", "CS203", "CS203", "MA101"],
    "Assessment Name": [
        "IA1 - Algorithms", "Assignment 1", "IA1 - DBMS", "Lab Review 1", "Semester Final Exam"
    ],
    "Type": [
        "Internal Assessment 1", "Assignment", "Internal Assessment 1", "Lab Review", "End Semester Exam"
    ],
    "Date": ["2026-11-09", "2026-11-18", "2026-11-10", "2026-11-22", "2026-12-10"],
    "Max Marks": [30, 10, 30, 20, 100],
    "Obtained Marks": [26, 9, 27, 18, 85],
    "Status": ["Scheduled", "Scheduled", "Scheduled", "Scheduled", "Scheduled"],
})

DEFAULT_SCORES = pd.DataFrame({
    "Semester": ["Semester 1", "Semester 1", "Semester 2", "Semester 2", "Semester 3", "Semester 3"],
    "Course Code": ["MA101", "PH101", "CS102", "EE101", "CS201", "EC202"],
    "Max Marks": [100, 100, 100, 100, 100, 100],
    "Obtained Score": [85, 78, 92, 80, 88, 76],
    "Grade": ["A", "B+", "A+", "A", "A", "B+"],
})

DEFAULT_CHECKLIST = pd.DataFrame({
    "category": [
        "Semester Preparation", "Assessments", "Projects", "Documents", "Placement",
    ],
    "item": [
        "Download current syllabus",
        "Prepare for IA1 - Data Structures",
        "Choose mini-project problem statement",
        "Update resume and marksheets folder",
        "Complete one aptitude mock test",
    ],
    "target_date": [
        "2026-11-03", "2026-11-09", "2026-11-12", "2026-12-01", "2026-11-15",
    ],
    "status": ["Done", "In Progress", "Not Started", "Not Started", "Not Started"],
    "notes": [
        "Verified from university portal",
        "Revise trees and graphs",
        "Discuss with lab partner",
        "Include latest Git repo link",
        "Aim for 80%+ quant score",
    ],
})


# =========================================================
# LOCAL CSV HELPER (KEPT FOR COMPATIBILITY)
# =========================================================
def load_data_file(filename, default_df):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df.columns = [str(col).strip() for col in df.columns]

            cols_lower = [c.lower() for c in df.columns]
            unique_indices = []
            seen = set()
            for idx, col in enumerate(cols_lower):
                if col not in seen:
                    seen.add(col)
                    unique_indices.append(idx)
            df = df.iloc[:, unique_indices]

            existing_lower = {c.lower(): c for c in df.columns}
            modified = False
            for col in default_df.columns:
                if col.lower() not in existing_lower:
                    if len(df) == 0:
                        df[col] = default_df[col]
                    elif len(df) <= len(default_df):
                        df[col] = default_df[col].iloc[:len(df)].values
                    else:
                        df[col] = default_df[col].iloc[0] if len(default_df) > 0 else ""
                    modified = True

            df = df.loc[:, ~df.columns.duplicated(keep="first")]
            if modified:
                df.to_csv(path, index=False)
            return df
        except Exception:
            return default_df.copy()

    default_df.to_csv(path, index=False)
    return default_df.copy()


# =========================================================
# AUTHENTICATION + SUPABASE DATA
# =========================================================
if not show_authentication():
    st.stop()

backend = get_backend()
logout_button()

calendar_filename = (
    "academic_calendar.csv"
    if os.path.exists(os.path.join(DATA_DIR, "academic_calendar.csv"))
    else "calendar.csv"
)

semesters_df = backend.load_dataframe("semesters", DEFAULT_SEMESTERS)
courses_df = backend.load_dataframe("courses", DEFAULT_COURSES)
univ_syllabus_df = backend.load_dataframe("university_syllabus", DEFAULT_UNIV_SYLLABUS)
calendar_df = backend.load_dataframe("calendar", DEFAULT_CALENDAR)
assessments_df = backend.load_dataframe("assessments", DEFAULT_ASSESSMENTS)
scores_df = backend.load_dataframe("scores", DEFAULT_SCORES)
checklist_df = backend.load_dataframe("plan_checklist", DEFAULT_CHECKLIST)

if "target_date" in checklist_df.columns:
    checklist_df["target_date"] = pd.to_datetime(
        checklist_df["target_date"], errors="coerce"
    ).dt.date

checklist_df.columns = [str(c).strip().lower() for c in checklist_df.columns]
checklist_df = checklist_df.loc[:, ~checklist_df.columns.duplicated(keep="first")]


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
st.sidebar.markdown(
    """
    <div style="padding: 8px 0 18px 0;">
        <div style="font-size: 30px;">🎓</div>
        <div style="font-size: 21px; font-weight: 850; color: #303B70;">
            Degree OS
        </div>
        <div style="font-size: 11px; color: #9299AF; letter-spacing: 1.2px;">
            YOUR ACADEMIC WORKSPACE
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

nav_options = [
    "1. Dashboard",
    "2. Semesters 1-8",
    "3. Courses & Syllabus",
    "4. University Syllabus",
    "5. Academic / Leave Calendar",
    "6. Internal Assessments",
    "7. Status Tracker",
    "8. Scorecard",
    "9. Plan & Checklist",
    "10. Ask Degree AI",
    "11. Data Admin",
]

# Guarantee state resets to "1. Dashboard" if cleared on sign-out
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "1. Dashboard"

selected_tab = st.sidebar.radio("NAVIGATION", nav_options, key="nav_selection")

st.sidebar.markdown("---")
st.sidebar.caption("STUDENT WORKSPACE")
st.sidebar.info("💡 Use **Data Admin** to manage your academic datasets.")
st.sidebar.markdown(
    """
    <div style="padding: 12px 2px; color: #A0A6B8; font-size: 11px;">
        MY ENGINEERING DEGREE OS<br>
        <span style="color:#777CE0;">BUILD SMALL. MAKE IT WORK.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# TAB 1 — DASHBOARD
# =========================================================
if selected_tab == "1. Dashboard":
    page_header(
        "YOUR ACADEMIC OVERVIEW",
        "Welcome to your Degree OS",
        "Your academic journey, progress and priorities — all in one place.",
        "👋",
    )

    target_series = pd.to_numeric(
        get_1d_series(semesters_df, "Target Credits", 0), errors="coerce"
    ).fillna(0)
    completed_series = pd.to_numeric(
        get_1d_series(semesters_df, "Completed Credits", 0), errors="coerce"
    ).fillna(0)

    total_target = target_series.sum() if target_series.sum() > 0 else 158
    total_completed = completed_series.sum()
    pct = round((total_completed / total_target) * 100, 1) if total_target else 0

    status_series = get_1d_series(semesters_df, "Status", "").astype(str).str.lower()
    in_prog = semesters_df[status_series == "in progress"]
    current_sem = "Not set"
    if not in_prog.empty:
        current_sem = str(in_prog.iloc[0].get("Semester", "Not set"))

    next_assessment = "None scheduled"
    if not assessments_df.empty:
        as_copy = assessments_df.copy()
        as_copy["PDate"] = pd.to_datetime(
            get_1d_series(as_copy, "Date", ""), errors="coerce"
        )
        upcoming = as_copy[as_copy["PDate"] >= today_dt].sort_values("PDate")
        if not upcoming.empty:
            next_assessment = (
                f"{upcoming.iloc[0].get('Assessment Name', 'Assessment')} "
                f"({upcoming.iloc[0].get('Date')})"
            )

    next_holiday = "None scheduled"
    if not calendar_df.empty:
        cal_copy = calendar_df.copy()
        type_col = get_1d_series(cal_copy, "Type", "").astype(str).str.lower()
        cal_copy["PDate"] = pd.to_datetime(
            get_1d_series(cal_copy, "Date", ""), errors="coerce"
        )
        leaves = cal_copy[type_col.str.contains("leave|holiday", na=False)]
        upcoming_leaves = leaves[leaves["PDate"] >= today_dt].sort_values("PDate")
        if not upcoming_leaves.empty:
            next_holiday = (
                f"{upcoming_leaves.iloc[0].get('Event Title', 'Holiday')} "
                f"({upcoming_leaves.iloc[0].get('Date')})"
            )

    obtained_scores = pd.to_numeric(
        get_1d_series(scores_df, "Obtained Score", 0), errors="coerce"
    ).fillna(0)
    maximum_scores = pd.to_numeric(
        get_1d_series(
            scores_df, "Max Marks",
            get_1d_series(scores_df, "Max Score", 0)
        ),
        errors="coerce",
    ).fillna(0)
    prototype_avg = (
        round((obtained_scores.sum() / maximum_scores.sum()) * 100, 2)
        if maximum_scores.sum() > 0 else 0.0
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current Semester", current_sem)
    m2.metric("Degree Completion", f"{pct}%", f"{int(total_completed)} / {int(total_target)} credits")
    m3.metric("Next Assessment", next_assessment)
    m4.metric("Prototype Score", f"{prototype_avg}%")

    st.markdown("")
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        with st.container(border=True):
            section_label("DEGREE JOURNEY")
            st.subheader("Your progress so far")
            st.write(f"**{pct}%** of the target credits recorded as completed")
            st.progress(min(max(pct / 100, 0), 1))
            st.caption(
                f"{int(total_completed)} completed credits out of "
                f"{int(total_target)} target credits."
            )

        with st.container(border=True):
            section_label("SEMESTER ROADMAP")
            st.subheader("Your eight-semester journey")
            roadmap = semesters_df.copy()
            for _, row in roadmap.iterrows():
                sem_name = row.get("Semester", "Semester")
                completed = pd.to_numeric(row.get("Completed Credits", 0), errors="coerce")
                target = pd.to_numeric(row.get("Target Credits", 0), errors="coerce")
                completed = 0 if pd.isna(completed) else completed
                target = 0 if pd.isna(target) else target
                ratio = min(completed / target, 1) if target > 0 else 0
                st.markdown(f"**{sem_name}** · {row.get('Status', 'N/A')}")
                st.progress(ratio)
                st.caption(f"{completed:g} / {target:g} credits · {row.get('Focus Area', '')}")

    with right:
        with st.container(border=True):
            section_label("UP NEXT")
            st.subheader("Academic priorities")
            st.markdown("**📝 Next assessment**")
            st.write(next_assessment)
            st.divider()
            st.markdown("**🌿 Next holiday / break**")
            st.write(next_holiday)

        with st.container(border=True):
            section_label("CHECKLIST HEALTH")
            st.subheader("Task status")
            
            chk_status = (
                get_1d_series(checklist_df, "status", "")
                .astype(str)
                .str.strip()
                .str.lower()
            )

            if not chk_status.empty and (chk_status != "").any():

                normalized_status = chk_status.replace({
                    "completed": "Done",
                    "done": "Done",
                    "in progress": "In Progress",
                    "not started": "Not Started",
                })

                status_order = ["Done", "In Progress", "Not Started"]

                status_counts = (
                    normalized_status
                    .value_counts()
                    .reindex(status_order, fill_value=0)
                )

                chart_df = pd.DataFrame({
                    "Task Status": status_counts.index,
                    "Tasks": status_counts.values,
                })

                chart_df = chart_df[chart_df["Tasks"] > 0]

                if not chart_df.empty:
                    color_map = {
                        "Done": "#55B99A",
                        "In Progress": "#8582E8",
                        "Not Started": "#F0AD78",
                    }

                    fig = px.pie(
                        chart_df,
                        names="Task Status",
                        values="Tasks",
                        hole=0.65,
                        color="Task Status",
                        color_discrete_map=color_map,
                    )

                    fig.update_traces(
                        textposition="outside",
                        textinfo="label+value",
                        marker=dict(
                            line=dict(color="#FFFFFF", width=4)
                        ),
                        hovertemplate=(
                            "<b>%{label}</b><br>"
                            "Tasks: %{value}<br>"
                            "Share: %{percent}"
                            "<extra></extra>"
                        ),
                    )

                    fig.update_layout(
                        showlegend=True,
                        legend_title_text="Task Status",
                        height=300,
                        margin=dict(l=10, r=10, t=15, b=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(
                            family="Arial",
                            color="#343B70",
                            size=12,
                        ),
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )

                else:
                    st.info("No checklist data available.")

            else:
                st.info("No checklist data available.")


    with st.container(border=True):
        section_label("ACADEMIC SNAPSHOT")
        st.subheader("Semester overview")
        st.dataframe(semesters_df, use_container_width=True, hide_index=True)


# =========================================================
# TAB 2 — SEMESTERS 1–8
# =========================================================
elif selected_tab == "2. Semesters 1-8":
    page_header(
        "DEGREE ROADMAP",
        "Semesters 1–8",
        "Explore milestones, credit progress and the focus area for each semester.",
        "📚",
    )

    for i in range(0, len(semesters_df), 2):
        cols = st.columns(2, gap="large")
        for j in range(2):
            if i + j < len(semesters_df):
                row = semesters_df.iloc[i + j]
                with cols[j]:
                    with st.container(border=True):
                        sem_name = row.get("Semester", f"Semester {i+j+1}")
                        status = row.get("Status", "N/A")
                        status_text = str(status).strip().lower()
                        if status_text == "completed":
                            pill_bg, pill_fg, status_icon = "#E5F7EF", "#21845D", "✓"
                        elif status_text == "in progress":
                            pill_bg, pill_fg, status_icon = "#EEEFFF", "#6268C9", "◉"
                        else:
                            pill_bg, pill_fg, status_icon = "#FFF2E7", "#B87935", "○"
                        st.markdown('<div class="colour-strip"></div>', unsafe_allow_html=True)
                        completed = pd.to_numeric(row.get("Completed Credits", 0), errors="coerce")
                        target = pd.to_numeric(row.get("Target Credits", 0), errors="coerce")
                        completed = 0 if pd.isna(completed) else completed
                        target = 0 if pd.isna(target) else target
                        ratio = min(completed / target, 1) if target > 0 else 0

                        st.markdown(f"### {sem_name}")
                        st.caption(str(row.get("Focus Area", "")))
                        st.markdown(
                            f'<span class="status-pill" style="background:{pill_bg};color:{pill_fg};">'
                            f'{status_icon} {status}</span>',
                            unsafe_allow_html=True,
                        )
                        st.progress(ratio)
                        st.caption(f"{completed:g} / {target:g} credits completed")

    st.markdown("")
    with st.container(border=True):
        section_label("CURRICULUM INSPECTOR")
        st.subheader("Inspect semester courses")
        all_sems = get_1d_series(semesters_df, "Semester", "").dropna().tolist()
        all_sems = [s for s in all_sems if s] or [f"Semester {i}" for i in range(1, 9)]
        sem_choice = st.selectbox("Choose a semester", all_sems)
        filtered = courses_df[
            get_1d_series(courses_df, "Semester", "") == sem_choice
        ]
        st.dataframe(filtered, use_container_width=True, hide_index=True)


# =========================================================
# TAB 3 — COURSES & SYLLABUS
# =========================================================
elif selected_tab == "3. Courses & Syllabus":
    page_header(
        "LEARNING LIBRARY",
        "Courses & Syllabus",
        "Browse course details, topics and credit allocations by semester.",
        "📖",
    )

    course_sems = sorted(
        get_1d_series(courses_df, "Semester", "").dropna().unique().tolist()
    )
    selected_sem = st.selectbox("Filter by semester", ["All"] + course_sems)

    display_df = courses_df.copy()
    if selected_sem != "All":
        display_df = display_df[
            get_1d_series(display_df, "Semester", "") == selected_sem
        ]

    a, b = st.columns(2)
    a.metric("Courses displayed", len(display_df))
    credit_total = pd.to_numeric(
        get_1d_series(display_df, "Credits", 0), errors="coerce"
    ).fillna(0).sum()
    b.metric("Credits in view", int(credit_total))

    with st.container(border=True):
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(display_df)} course(s) for: {selected_sem}")


# =========================================================
# TAB 4 — UNIVERSITY SYLLABUS
# =========================================================
elif selected_tab == "4. University Syllabus":
    page_header(
        "REFERENCE CENTRE",
        "University Syllabus",
        "Programme-level information and the syllabus reference stored in your workspace.",
        "🏛️",
    )

    if not univ_syllabus_df.empty:
        row = univ_syllabus_df.iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Total semesters", str(row.get("Total Semesters", "8")))
        c2.metric("Total credits required", str(row.get("Total Credits Required", "N/A")))
        c3.metric("Curriculum version", str(row.get("Curriculum Version", "N/A")))

        with st.container(border=True):
            section_label("PROGRAMME")
            st.subheader(str(row.get("Programme", "N/A")))
            st.write(str(row.get("Program Overview", "No programme overview available.")))

        with st.container(border=True):
            section_label("SOURCE / REFERENCE")
            st.code(
                str(row.get("Syllabus Source / Reference", "No source recorded.")),
                language="text",
            )
            st.caption("Check the institution's official portal to verify current regulations.")

        with st.container(border=True):
            st.subheader("Stored syllabus record")
            st.dataframe(univ_syllabus_df, use_container_width=True, hide_index=True)
    else:
        st.warning("University syllabus record is empty.")


# =========================================================
# TAB 5 — ACADEMIC / LEAVE CALENDAR
# =========================================================
elif selected_tab == "5. Academic / Leave Calendar":
    page_header(
        "DATES THAT MATTER",
        "Academic & Leave Calendar",
        "Keep academic events, assessments and breaks in one organised view.",
        "🗓️",
    )

    col1, col2 = st.columns(2)
    years = sorted(get_1d_series(calendar_df, "Academic Year", "").dropna().unique().tolist())
    sems = sorted(get_1d_series(calendar_df, "Semester", "").dropna().unique().tolist())

    with col1:
        year_filter = st.selectbox("Academic year", ["All"] + years)
    with col2:
        sem_filter = st.selectbox("Semester", ["All"] + sems)

    cal_view = calendar_df.copy()
    if year_filter != "All":
        cal_view = cal_view[get_1d_series(cal_view, "Academic Year", "") == year_filter]
    if sem_filter != "All":
        cal_view = cal_view[get_1d_series(cal_view, "Semester", "") == sem_filter]

    with st.container(border=True):
        section_label("EVENT SCHEDULE")
        st.subheader(f"{len(cal_view)} event(s)")
        if not cal_view.empty:
            st.dataframe(cal_view, use_container_width=True, hide_index=True)
        else:
            st.info("No events match these filters.")


# =========================================================
# TAB 6 — INTERNAL ASSESSMENTS
# =========================================================
elif selected_tab == "6. Internal Assessments":
    page_header(
        "ASSESSMENT CENTRE",
        "Internal Assessments",
        "Track IA tests, assignments, lab reviews and examination marks.",
        "📝",
    )

    max_m = pd.to_numeric(
        get_1d_series(assessments_df, "Max Marks", 0), errors="coerce"
    ).fillna(0)
    obt_m = pd.to_numeric(
        get_1d_series(assessments_df, "Obtained Marks", 0), errors="coerce"
    ).fillna(0)
    total_max = max_m.sum()
    total_obt = obt_m.sum()
    pct_secured = round((total_obt / total_max) * 100, 1) if total_max > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Recorded assessments", len(assessments_df))
    c2.metric("Marks recorded", f"{total_obt:g} / {total_max:g}")
    c3.metric("Recorded percentage", f"{pct_secured}%")

    with st.container(border=True):
        section_label("ASSESSMENT REGISTER")
        st.dataframe(assessments_df, use_container_width=True, hide_index=True)


# =========================================================
# TAB 7 — STATUS TRACKER
# =========================================================
elif selected_tab == "7. Status Tracker":
    page_header(
        "PROGRESS MONITOR",
        "Academic Status Tracker",
        "See how your courses are progressing within a selected semester.",
        "📋",
    )

    course_sems = sorted(
        get_1d_series(courses_df, "Semester", "").dropna().unique().tolist()
    ) or [f"Semester {i}" for i in range(1, 9)]

    target_sem = st.selectbox(
        "Select semester to track",
        course_sems,
        index=min(2, len(course_sems) - 1),
    )

    sem_courses = courses_df[
        get_1d_series(courses_df, "Semester", "") == target_sem
    ].copy()
    status_series = get_1d_series(sem_courses, "Status", "").astype(str).str.lower()

    completed_count = (status_series == "completed").sum()
    in_progress_count = (status_series == "in progress").sum()
    not_started_count = (status_series == "not started").sum()
    total_courses = len(sem_courses)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total courses", total_courses)
    c2.metric("Completed", completed_count)
    c3.metric("In progress", in_progress_count)
    c4.metric("Not started", not_started_count)

    progress_ratio = completed_count / total_courses if total_courses else 0
    with st.container(border=True):
        section_label("SEMESTER COMPLETION")
        st.subheader(f"{target_sem}: {round(progress_ratio * 100, 1)}% complete")
        st.progress(progress_ratio)
        st.dataframe(sem_courses, use_container_width=True, hide_index=True)


# =========================================================
# TAB 8 — SCORECARD
# =========================================================
elif selected_tab == "8. Scorecard":
    page_header(
        "PERFORMANCE OVERVIEW",
        "Academic Scorecard",
        "Review recorded marks and course-wise grades in your workspace.",
        "🏆",
    )

    obtained = pd.to_numeric(
        get_1d_series(scores_df, "Obtained Score", 0), errors="coerce"
    ).fillna(0)
    maximum = pd.to_numeric(
        get_1d_series(
            scores_df, "Max Marks",
            get_1d_series(scores_df, "Max Score", 0)
        ),
        errors="coerce",
    ).fillna(0)

    sum_obtained = obtained.sum()
    sum_maximum = maximum.sum()
    simple_pct = round((sum_obtained / sum_maximum) * 100, 2) if sum_maximum > 0 else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Courses with scores", len(scores_df))
    c2.metric("Marks recorded", f"{sum_obtained:g} / {sum_maximum:g}")
    c3.metric("Prototype percentage", f"{simple_pct}%")

    with st.container(border=True):
        section_label("COURSE PERFORMANCE")
        st.dataframe(scores_df, use_container_width=True, hide_index=True)

    st.warning(
        "This is a prototype score percentage, NOT an official university CGPA. "
        "Official CGPA regulations are not applied without validated institutional rules."
    )


# =========================================================
# TAB 9 — PLAN & CHECKLIST
# =========================================================
elif selected_tab == "9. Plan & Checklist":
    page_header(
        "PERSONAL EXECUTION PLAN",
        "Plan & Checklist",
        "Organise semester preparation, assignments, projects and placement tasks.",
        "✅",
    )

    checklist_work = checklist_df.copy()
    checklist_work["p_date"] = pd.to_datetime(
        get_1d_series(checklist_work, "target_date", ""), errors="coerce"
    )
    status_col = get_1d_series(checklist_work, "status", "").astype(str).str.lower()

    total_items = len(checklist_work)
    done_count = (status_col == "done").sum()
    not_done = checklist_work[status_col != "done"]
    not_done_dates = pd.to_datetime(
        get_1d_series(not_done, "target_date", ""), errors="coerce"
    )
    overdue_count = (not_done_dates < today_dt).sum()
    due_soon_count = (
        (not_done_dates >= today_dt)
        & (not_done_dates <= today_dt + pd.Timedelta(days=7))
    ).sum()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total tasks", total_items)
    m2.metric("Completed", done_count)
    m3.metric("Due in 7 days", due_soon_count)
    m4.metric("Overdue", overdue_count)

    with st.container(border=True):
        section_label("TASK MANAGER")
        st.subheader("Edit your checklist")
        st.caption("Allowed status values: Not Started · In Progress · Done")

        edited_checklist = st.data_editor(
            checklist_df,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Not Started", "In Progress", "Done"],
                    required=True,
                ),
                "target_date": st.column_config.DateColumn("Target Date"),
                "category": st.column_config.SelectboxColumn(
                    "Category",
                    options=[
                        "Semester Preparation", "Assessments", "Labs",
                        "Projects", "Documents", "Skills", "Placement",
                    ],
                ),
            },
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="checklist_editor",
        )

        if st.button("Save Plan & Checklist", type="primary", key="save_checklist"):
            clean_save = edited_checklist.loc[
                :, ~edited_checklist.columns.duplicated(keep="first")
            ].copy()
            if "target_date" in clean_save.columns:
                clean_save["target_date"] = clean_save["target_date"].apply(safe_date_string)
            backend.save_dataframe("plan_checklist", clean_save)
            st.success("Changes saved to your Supabase account.")
            st.rerun()

    st.markdown("")
    section_label("FOCUS VIEWS")
    tab_week, tab_sem, tab_degree = st.tabs(
        ["⚡ This Week", "🎯 Semester Milestones", "🚀 Degree & Placement"]
    )

    with tab_week:
        this_week = checklist_work[
            (checklist_work["p_date"] >= today_dt)
            & (checklist_work["p_date"] <= today_dt + pd.Timedelta(days=7))
        ]
        st.dataframe(
            this_week[["category", "item", "target_date", "status", "notes"]],
            use_container_width=True,
            hide_index=True,
        )

    with tab_sem:
        categories = get_1d_series(checklist_work, "category", "")
        sem_tasks = checklist_work[
            categories.isin(["Semester Preparation", "Assessments", "Labs", "Projects"])
        ]
        st.dataframe(
            sem_tasks[["category", "item", "target_date", "status", "notes"]],
            use_container_width=True,
            hide_index=True,
        )

    with tab_degree:
        categories = get_1d_series(checklist_work, "category", "")
        degree_tasks = checklist_work[
            categories.isin(["Documents", "Skills", "Placement"])
        ]
        st.dataframe(
            degree_tasks[["category", "item", "target_date", "status", "notes"]],
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# TAB 10 — ASK DEGREE AI
# =========================================================
elif selected_tab == "10. Ask Degree AI":
    page_header(
        "YOUR ACADEMIC COPILOT",
        "Ask Degree AI",
        "Ask questions about the academic information stored in your Degree OS.",
        "🤖",
    )

    api_key = st.secrets.get(
        "GEMINI_API_KEY",
        os.environ.get("GEMINI_API_KEY", ""),
    )

    context_data = f"""
Degree Data Source of Truth:

[SEMESTERS]
{semesters_df.to_string(index=False)}

[COURSES]
{courses_df.to_string(index=False)}

[CALENDAR]
{calendar_df.to_string(index=False)}

[ASSESSMENTS]
{assessments_df.to_string(index=False)}

[SCORES]
{scores_df.to_string(index=False)}

[CHECKLIST]
{checklist_df.to_string(index=False)}
"""

    with st.container(border=True):
        section_label("QUICK PROMPTS")
        st.caption("Choose a question to get started.")
        quick_cols = st.columns(5)
        quick_prompts = [
            "What courses are still incomplete in Semester 3?",
            "When is my next internal assessment?",
            "Show my next holiday",
            "What topics are in Data Structures?",
            "What is my official university CGPA formula?",
        ]
        quick_labels = [
            "Incomplete courses",
            "Next assessment",
            "Next holiday",
            "Data Structures",
            "CGPA rules",
        ]
        selected_prompt = None
        for index, col in enumerate(quick_cols):
            if col.button(quick_labels[index], key=f"quick_prompt_{index}", use_container_width=True):
                selected_prompt = quick_prompts[index]

    user_query = st.text_input(
        "Your question",
        value=selected_prompt or "",
        placeholder="e.g. What should I prepare for my next assessment?",
    )

    if user_query:
        query_norm = user_query.strip().lower()
        unsupported_keywords = [
            "cgpa formula", "official formula", "exam regulation",
            "eligibility rule", "attendance policy",
        ]
        is_unsupported = any(word in query_norm for word in unsupported_keywords)

        if is_unsupported:
            st.warning("Data Area Used: None")
            st.error("I cannot verify that from the current Degree OS data.")
            st.caption(
                "Institutional regulations and CGPA formulas are not inferred "
                "without an authoritative source document."
            )

        elif api_key and GEMINI_AVAILABLE:
            with st.spinner("Degree AI is reviewing your academic data..."):
                try:
                    client = genai.Client(api_key=api_key)
                    system_instruction = (
                        "You are Degree AI. Answer only from the supplied degree data. "
                        "Do not invent university rules, dates, marks, formulas or syllabus content. "
                        "If information is missing, say: I cannot verify that from the current "
                        "Degree OS data. At the end, state which data area was used: Courses, "
                        "Calendar, Assessments, Scores, Plan, Semesters, or None."
                    )
                    prompt_content = f"{context_data}\n\nStudent Question: {user_query}"

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt_content,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.0,
                        ),
                    )
                    st.markdown("### Degree AI Answer")
                    st.markdown(response.text or "The AI returned an empty response.")
                except Exception as error:
                    st.error(f"Gemini API query error: {error}")
                    api_key = ""

        if (not api_key or not GEMINI_AVAILABLE) and not is_unsupported:
            st.markdown("### Degree AI Answer")

            if "incomplete" in query_norm or (
                "courses" in query_norm and "semester 3" in query_norm
            ):
                st.info("Data Area Used: Courses")
                sem_series = get_1d_series(courses_df, "Semester", "")
                stat_series = get_1d_series(courses_df, "Status", "")
                sem3_incomplete = courses_df[
                    (sem_series == "Semester 3") & (stat_series != "Completed")
                ]
                if not sem3_incomplete.empty:
                    st.write("These Semester 3 courses are not marked as completed:")
                    for _, row in sem3_incomplete.iterrows():
                        st.write(
                            f"- **{row.get('Course Code')}** — "
                            f"{row.get('Course Title')} ({row.get('Status')})"
                        )
                else:
                    st.write("All Semester 3 courses are marked as completed.")

            elif "assessment" in query_norm or "ia" in query_norm or "exam" in query_norm:
                st.info("Data Area Used: Assessments")
                if not assessments_df.empty:
                    assessment_copy = assessments_df.copy()
                    assessment_copy["PDate"] = pd.to_datetime(
                        get_1d_series(assessment_copy, "Date", ""), errors="coerce"
                    )
                    upcoming = assessment_copy[
                        assessment_copy["PDate"] >= today_dt
                    ].sort_values("PDate")
                    if not upcoming.empty:
                        row = upcoming.iloc[0]
                        st.write(
                            f"Your next assessment is **{row.get('Assessment Name')}** "
                            f"({row.get('Course Code')}) on **{row.get('Date')}**."
                        )
                    else:
                        st.write("No upcoming assessment is recorded.")
                else:
                    st.write("I cannot verify that from the current Degree OS data.")

            elif "holiday" in query_norm or "leave" in query_norm or "break" in query_norm:
                st.info("Data Area Used: Calendar")
                if not calendar_df.empty:
                    calendar_copy = calendar_df.copy()
                    calendar_copy["PDate"] = pd.to_datetime(
                        get_1d_series(calendar_copy, "Date", ""), errors="coerce"
                    )
                    event_types = get_1d_series(
                        calendar_copy, "Type", ""
                    ).astype(str).str.lower()
                    leaves = calendar_copy[
                        event_types.str.contains("leave|holiday", na=False)
                    ]
                    upcoming_leaves = leaves[
                        leaves["PDate"] >= today_dt
                    ].sort_values("PDate")
                    if not upcoming_leaves.empty:
                        row = upcoming_leaves.iloc[0]
                        st.write(
                            f"Your next holiday is **{row.get('Event Title')}** "
                            f"on **{row.get('Date')}**."
                        )
                    elif not leaves.empty:
                        st.write("No upcoming holiday is recorded.")
                    else:
                        st.write("No holidays are recorded in your calendar.")
                else:
                    st.write("I cannot verify that from the current Degree OS data.")

            elif (
                "data structures" in query_norm
                or "syllabus" in query_norm
                or "topics" in query_norm
            ):
                st.info("Data Area Used: Courses")
                title_series = get_1d_series(
                    courses_df, "Course Title", ""
                ).astype(str)
                ds_course = courses_df[
                    title_series.str.contains("Data Structures", case=False, na=False)
                ]
                if not ds_course.empty:
                    row = ds_course.iloc[0]
                    st.write(
                        f"Topics in **Data Structures ({row.get('Course Code')})**:"
                    )
                    st.markdown(f"> {row.get('Syllabus Topics', 'N/A')}")
                else:
                    st.write("I cannot verify that from the current Degree OS data.")

            elif "checklist" in query_norm or "task" in query_norm or "plan" in query_norm:
                st.info("Data Area Used: Plan")
                st.write(f"{len(checklist_df)} tasks are recorded. Pending tasks:")
                status_values = get_1d_series(
                    checklist_df, "status", ""
                ).astype(str).str.lower()
                pending = checklist_df[status_values != "done"]
                for _, row in pending.iterrows():
                    st.write(
                        f"- [{row.get('status')}] **{row.get('item')}** "
                        f"(Target: {row.get('target_date')})"
                    )

            elif "semester" in query_norm:
                st.info("Data Area Used: Semesters")
                st.dataframe(
                    semesters_df[
                        ["Semester", "Status", "Completed Credits", "Target Credits"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.info("Data Area Used: None")
                st.write("I cannot verify that from the current Degree OS data.")


# =========================================================
# TAB 11 — DATA ADMIN
# =========================================================
elif selected_tab == "11. Data Admin":
    page_header(
        "WORKSPACE SETTINGS",
        "Data Administrator",
        "Edit or restore the datasets that power your Degree OS.",
        "🛠️",
    )

    table_options = {
        "semesters.csv": (semesters_df, DEFAULT_SEMESTERS),
        "courses.csv": (courses_df, DEFAULT_COURSES),
        "university_syllabus.csv": (univ_syllabus_df, DEFAULT_UNIV_SYLLABUS),
        calendar_filename: (calendar_df, DEFAULT_CALENDAR),
        "assessments.csv": (assessments_df, DEFAULT_ASSESSMENTS),
        "scores.csv": (scores_df, DEFAULT_SCORES),
        "plan_checklist.csv": (checklist_df, DEFAULT_CHECKLIST),
    }

    dataset_choice = st.selectbox("Choose a dataset", list(table_options.keys()))
    df_to_edit, default_blueprint = table_options[dataset_choice]

    dataset_name_map = {
        "semesters.csv": "semesters",
        "courses.csv": "courses",
        "university_syllabus.csv": "university_syllabus",
        "academic_calendar.csv": "calendar",
        "calendar.csv": "calendar",
        "assessments.csv": "assessments",
        "scores.csv": "scores",
        "plan_checklist.csv": "plan_checklist",
    }
    dataset_name = dataset_name_map[dataset_choice]

    with st.container(border=True):
        section_label("DATASET EDITOR")
        st.subheader(f"Editing {dataset_choice}")
        edited_data = st.data_editor(
            df_to_edit,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key=f"admin_editor_{dataset_choice}",
        )

        save_col, reset_col = st.columns([1, 2])
        with save_col:
            if st.button("Save changes", type="primary", key="admin_save"):
                clean_edited = edited_data.loc[
                    :, ~edited_data.columns.duplicated(keep="first")
                ].copy()
                if dataset_name == "plan_checklist" and "target_date" in clean_edited.columns:
                    clean_edited["target_date"] = clean_edited["target_date"].apply(
                        safe_date_string
                    )
                backend.save_dataframe(dataset_name, clean_edited)
                st.success(f"Successfully updated {dataset_choice} in Supabase.")
                st.rerun()

        with reset_col:
            if st.button("Reset to blueprint template", key="admin_reset"):
                backend.save_dataframe(dataset_name, default_blueprint)
                st.warning(f"{dataset_choice} was reset to its default template.")
                st.rerun()
