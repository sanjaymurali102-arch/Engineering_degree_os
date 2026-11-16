import os
import datetime
import pandas as pd
import streamlit as st

# Safe import for Gemini SDK
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ==========================================
# PAGE CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="My Engineering Degree OS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
today_dt = pd.Timestamp(datetime.date.today())

# ==========================================
# DEFAULT DATASETS (RUBRIC-ALIGNED)
# ==========================================
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
        "Semester Preparation",
        "Assessments",
        "Projects",
        "Documents",
        "Placement",
    ],
    "item": [
        "Download current syllabus",
        "Prepare for IA1 - Data Structures",
        "Choose mini-project problem statement",
        "Update resume and marksheets folder",
        "Complete one aptitude mock test",
    ],
    "target_date": [
        "2026-11-03",
        "2026-11-09",
        "2026-11-12",
        "2026-12-01",
        "2026-11-15",
    ],
    "status": [
        "Done",
        "In Progress",
        "Not Started",
        "Not Started",
        "Not Started",
    ],
    "notes": [
        "Verified from university portal",
        "Revise trees and graphs",
        "Discuss with lab partner",
        "Include latest Git repo link",
        "Aim for 80%+ quant score",
    ],
})

# ==========================================
# BULLETPROOF DATA LOADER (SOLVES 1D GROUPER & KEYERROR)
# ==========================================
def load_data_file(filename, default_df):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            # 1. Clean whitespace from all column names
            df.columns = [str(col).strip() for col in df.columns]

            # 2. Case-insensitive column deduplication (keeps first occurrence)
            cols_lower = [c.lower() for c in df.columns]
            unique_indices = []
            seen = set()
            for idx, c in enumerate(cols_lower):
                if c not in seen:
                    seen.add(c)
                    unique_indices.append(idx)
            df = df.iloc[:, unique_indices]

            # 3. Add default columns only if missing
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

            # Drop any remaining exact duplicate headers
            df = df.loc[:, ~df.columns.duplicated(keep="first")]

            if modified:
                df.to_csv(path, index=False)
            return df
        except Exception:
            return default_df.copy()
    else:
        default_df.to_csv(path, index=False)
        return default_df.copy()

# Check for either calendar filename
calendar_filename = "academic_calendar.csv" if os.path.exists(os.path.join(DATA_DIR, "academic_calendar.csv")) else "calendar.csv"

semesters_df = load_data_file("semesters.csv", DEFAULT_SEMESTERS)
courses_df = load_data_file("courses.csv", DEFAULT_COURSES)
univ_syllabus_df = load_data_file("university_syllabus.csv", DEFAULT_UNIV_SYLLABUS)
calendar_df = load_data_file(calendar_filename, DEFAULT_CALENDAR)
assessments_df = load_data_file("assessments.csv", DEFAULT_ASSESSMENTS)
scores_df = load_data_file("scores.csv", DEFAULT_SCORES)
checklist_df = load_data_file("plan_checklist.csv", DEFAULT_CHECKLIST)

# Standardize checklist headers to lowercase and force single dimensional columns
checklist_df.columns = [str(c).strip().lower() for c in checklist_df.columns]
checklist_df = checklist_df.loc[:, ~checklist_df.columns.duplicated(keep="first")]

# Helper to safely extract a 1D series from any DataFrame
def get_1d_series(df, col_name, fallback_val=""):
    matching_cols = [c for c in df.columns if str(c).strip().lower() == str(col_name).strip().lower()]
    if matching_cols:
        series_obj = df[matching_cols[0]]
        if isinstance(series_obj, pd.DataFrame):
            return series_obj.iloc[:, 0]
        return series_obj
    return pd.Series([fallback_val] * len(df))

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🎓 Engineering Degree OS")
st.sidebar.caption("Build small. Make it work. Launch it.")
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

selected_tab = st.sidebar.radio("Navigation", nav_options)
st.sidebar.markdown("---")
st.sidebar.info("💡 **Phase 7 Tip:** Use **Data Admin** to test live changes without touching code.")

# ==========================================
# TAB 1: DASHBOARD
# ==========================================
if selected_tab == "1. Dashboard":
    st.title("📊 Engineering Degree Dashboard")
    st.markdown("Your central academic cockpit and degree progress metrics.")

    # Credits metric
    target_series = pd.to_numeric(get_1d_series(semesters_df, "Target Credits", 0), errors="coerce").fillna(0)
    completed_series = pd.to_numeric(get_1d_series(semesters_df, "Completed Credits", 0), errors="coerce").fillna(0)
    total_target = target_series.sum() if target_series.sum() > 0 else 158
    total_completed = completed_series.sum()
    pct = round((total_completed / total_target) * 100, 1)

    # Current semester
    status_series = get_1d_series(semesters_df, "Status", "").astype(str).str.lower()
    in_prog = semesters_df[status_series == "in progress"]
    current_sem = "Semester 4"
    if not in_prog.empty:
        current_sem = str(in_prog.iloc[0].get("Semester", "Semester 4"))

    # Next assessment
    next_assessment = "None scheduled"
    if not assessments_df.empty:
        as_copy = assessments_df.copy()
        date_col = get_1d_series(as_copy, "Date", "")
        as_copy["PDate"] = pd.to_datetime(date_col, errors="coerce")
        upcoming = as_copy[as_copy["PDate"] >= today_dt].sort_values("PDate")
        if not upcoming.empty:
            next_assessment = f"{upcoming.iloc[0].get('Assessment Name', 'Assessment')} ({upcoming.iloc[0].get('Date')})"
        elif len(as_copy) > 0:
            next_assessment = f"{as_copy.iloc[0].get('Assessment Name', 'Assessment')} ({as_copy.iloc[0].get('Date')})"

    # Next holiday
    next_holiday = "None scheduled"
    if not calendar_df.empty:
        cal_copy = calendar_df.copy()
        type_col = get_1d_series(cal_copy, "Type", "").astype(str).str.lower()
        date_col = get_1d_series(cal_copy, "Date", "")
        cal_copy["PDate"] = pd.to_datetime(date_col, errors="coerce")
        leaves = cal_copy[type_col.str.contains("leave|holiday", na=False)]
        upcoming_leaves = leaves[leaves["PDate"] >= today_dt].sort_values("PDate")
        if not upcoming_leaves.empty:
            next_holiday = f"{upcoming_leaves.iloc[0].get('Event Title', 'Holiday')} ({upcoming_leaves.iloc[0].get('Date')})"
        elif not leaves.empty:
            next_holiday = f"{leaves.iloc[0].get('Event Title', 'Holiday')} ({leaves.iloc[0].get('Date')})"

    # Score calculation
    obt_series = pd.to_numeric(get_1d_series(scores_df, "Obtained Score", 0), errors="coerce").fillna(0)
    max_series = pd.to_numeric(get_1d_series(scores_df, "Max Marks", get_1d_series(scores_df, "Max Score", 0)), errors="coerce").fillna(0)
    prototype_avg = 0.0
    if max_series.sum() > 0:
        prototype_avg = round((obt_series.sum() / max_series.sum()) * 100, 2)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Semester", current_sem)
    c2.metric("Degree Completion", f"{pct}%", f"{int(total_completed)}/{int(total_target)} Credits")
    c3.metric("Next Assessment", next_assessment)
    c4.metric("Prototype Score %", f"{prototype_avg}%")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🗓️ Next Academic Event / Break")
        st.info(f"**Upcoming Leave/Holiday:** {next_holiday}")
        
        st.subheader("📋 Checklist Quick Health")
        chk_status = get_1d_series(checklist_df, "status", "")
        if not chk_status.empty and (chk_status != "").any():
            st.bar_chart(chk_status.value_counts())
        else:
            st.info("No checklist data available.")
            
    with col_b:
        st.subheader("📈 Degree Semesters Roadmap")
        st.dataframe(semesters_df, use_container_width=True)

# ==========================================
# TAB 2: SEMESTERS 1-8 (PHASE 4)
# ==========================================
elif selected_tab == "2. Semesters 1-8":
    st.title("📚 Semesters 1 to 8 Overview")
    st.markdown("All eight degree semesters represented with milestones, credits, and status.")

    for i in range(0, len(semesters_df), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(semesters_df):
                row = semesters_df.iloc[i + j]
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"### {row.get('Semester', f'Semester {i+j+1}')}")
                        st.markdown(f"**Status:** `{row.get('Status', 'N/A')}`")
                        st.markdown(f"**Credits:** {row.get('Completed Credits', 0)} / {row.get('Target Credits', 0)}")
                        st.caption(f"🎯 {row.get('Focus Area', '')}")

    st.markdown("---")
    st.subheader("🔍 Inspect Semester Curriculum")
    sem_col = get_1d_series(semesters_df, "Semester", "")
    all_sems = [s for s in sem_col.tolist() if s] or [f"Semester {i}" for i in range(1, 9)]
    sem_choice = st.selectbox("Select Semester", all_sems)
    
    courses_sem_col = get_1d_series(courses_df, "Semester", "")
    filtered = courses_df[courses_sem_col == sem_choice]
    st.dataframe(filtered, use_container_width=True)

# ==========================================
# TAB 3: COURSES & SYLLABUS (PHASE 4)
# ==========================================
elif selected_tab == "3. Courses & Syllabus":
    st.title("📖 Courses & Syllabus")
    st.markdown("Filter courses across semesters to verify topics and credit allocations.")

    course_sems = sorted(get_1d_series(courses_df, "Semester", "").dropna().unique().tolist())
    selected_sem = st.selectbox("Select Semester (Verify table updates dynamically)", ["All"] + course_sems)

    display_df = courses_df.copy()
    if selected_sem != "All":
        sem_series = get_1d_series(display_df, "Semester", "")
        display_df = display_df[sem_series == selected_sem]

    st.dataframe(display_df, use_container_width=True)
    if not display_df.empty:
        st.caption(f"Showing {len(display_df)} course(s) for selection: **{selected_sem}**")

# ==========================================
# TAB 4: UNIVERSITY SYLLABUS (PHASE 4)
# ==========================================
elif selected_tab == "4. University Syllabus":
    st.title("🏛️ University Syllabus Reference")
    st.markdown("Programme-level summary and official handbook reference. *(No invented regulations)*.")

    if not univ_syllabus_df.empty:
        row = univ_syllabus_df.iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Degree Programme", str(row.get("Programme", "N/A")))
            st.metric("Total Semesters", str(row.get("Total Semesters", "8")))
        with col2:
            st.metric("Expected Total Credits", str(row.get("Total Credits Required", "158")))
            st.metric("Curriculum Version", str(row.get("Curriculum Version", "N/A")))

        st.markdown("---")
        st.subheader("Official Syllabus Source / Reference")
        st.code(str(row.get("Syllabus Source / Reference", "University Handbook v4.2")), language="text")

        st.subheader("Program Overview")
        st.info(str(row.get("Program Overview", "Curriculum handbook outline.")))
        st.dataframe(univ_syllabus_df, use_container_width=True)
    else:
        st.warning("University syllabus record is empty.")

# ==========================================
# TAB 5: ACADEMIC / LEAVE CALENDAR (PHASE 4)
# ==========================================
elif selected_tab == "5. Academic / Leave Calendar":
    st.title("🗓️ Academic & Leave Calendar")
    st.markdown("Academic events, internal assessments, and holidays coexist with clear filtering.")

    col1, col2 = st.columns(2)
    with col1:
        years = sorted(get_1d_series(calendar_df, "Academic Year", "").dropna().unique().tolist())
        year_filter = st.selectbox("Filter by Academic Year", ["All"] + years)
    with col2:
        sems = sorted(get_1d_series(calendar_df, "Semester", "").dropna().unique().tolist())
        sem_filter = st.selectbox("Filter by Semester", ["All"] + sems)

    cal_view = calendar_df.copy()
    if year_filter != "All":
        y_col = get_1d_series(cal_view, "Academic Year", "")
        cal_view = cal_view[y_col == year_filter]
    if sem_filter != "All":
        s_col = get_1d_series(cal_view, "Semester", "")
        cal_view = cal_view[s_col == sem_filter]

    st.dataframe(cal_view, use_container_width=True)

# ==========================================
# TAB 6: INTERNAL ASSESSMENTS (PHASE 4)
# ==========================================
elif selected_tab == "6. Internal Assessments":
    st.title("📝 Internal Assessments & Evaluations")
    st.markdown("Tracks IA1, IA2, assignments, lab reviews, and semester examinations.")

    st.dataframe(assessments_df, use_container_width=True)
    max_m = pd.to_numeric(get_1d_series(assessments_df, "Max Marks", 0), errors="coerce").fillna(0)
    obt_m = pd.to_numeric(get_1d_series(assessments_df, "Obtained Marks", 0), errors="coerce").fillna(0)
    
    t_max = max_m.sum()
    t_obt = obt_m.sum()
    pct_secured = round((t_obt / t_max) * 100, 1) if t_max > 0 else 0
    st.metric("Total Assessment Marks Secured", f"{int(t_obt)} / {int(t_max)}", f"{pct_secured}%")

# ==========================================
# TAB 7: STATUS TRACKER (PHASE 5)
# ==========================================
elif selected_tab == "7. Status Tracker":
    st.title("📋 Academic Status Tracker")
    st.markdown("Track completion and progress by semester.")

    course_sems = sorted(get_1d_series(courses_df, "Semester", "").dropna().unique().tolist()) or [f"Semester {i}" for i in range(1, 9)]
    target_sem = st.selectbox("Select Semester to Track", course_sems, index=min(2, len(course_sems)-1))

    sem_courses = courses_df[get_1d_series(courses_df, "Semester", "") == target_sem].copy()
    status_series = get_1d_series(sem_courses, "Status", "").astype(str)

    c_completed = (status_series == "Completed").sum()
    c_in_progress = (status_series == "In Progress").sum()
    c_not_started = (status_series == "Not Started").sum()
    total_sem_courses = len(sem_courses)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Courses", total_sem_courses)
    c2.metric("Completed", c_completed)
    c3.metric("In Progress", c_in_progress)
    c4.metric("Not Started", c_not_started)

    progress_ratio = (c_completed / total_sem_courses) if total_sem_courses > 0 else 0.0
    st.write(f"**{target_sem} Completion Progress ({round(progress_ratio * 100, 1)}%)**")
    st.progress(progress_ratio)

    st.markdown("---")
    st.subheader(f"Courses for {target_sem}")
    st.dataframe(sem_courses, use_container_width=True)

# ==========================================
# TAB 8: SCORECARD (PHASE 5)
# ==========================================
elif selected_tab == "8. Scorecard":
    st.title("🏆 Academic Scorecard & Grades")
    st.markdown("Course-wise grades and simple percentage calculated from loaded sample data.")

    st.dataframe(scores_df, use_container_width=True)

    obt = pd.to_numeric(get_1d_series(scores_df, "Obtained Score", 0), errors="coerce").fillna(0)
    max_m = pd.to_numeric(get_1d_series(scores_df, "Max Marks", get_1d_series(scores_df, "Max Score", 0)), errors="coerce").fillna(0)

    sum_obt = obt.sum()
    sum_max = max_m.sum()
    simple_pct = round((sum_obt / sum_max) * 100, 2) if sum_max > 0 else 0.0

    st.markdown("---")
    st.metric(
        label="prototype score percentage",
        value=f"{simple_pct}%",
        help="Calculated as: (Total Obtained Marks / Total Max Marks) * 100."
    )
    st.warning("⚠️ **Important:** This is a **prototype score percentage**, NOT an official university CGPA formula. Official CGPA regulations are not applied without validated institutional rules.")

# ==========================================
# TAB 9: PLAN & CHECKLIST (PHASE 5)
# ==========================================
elif selected_tab == "9. Plan & Checklist":
    st.title("✅ Degree Execution Plan & Checklist")
    st.markdown("Your degree execution control panel. Manage weekly tasks, milestones, and preparation.")

    checklist_work = checklist_df.copy()
    date_col = get_1d_series(checklist_work, "target_date", "")
    checklist_work["p_date"] = pd.to_datetime(date_col, errors="coerce")
    status_col = get_1d_series(checklist_work, "status", "").astype(str).str.lower()
    
    total_items = len(checklist_work)
    done_count = (status_col == "done").sum()
    not_done = checklist_work[status_col != "done"]
    
    not_done_dates = pd.to_datetime(get_1d_series(not_done, "target_date", ""), errors="coerce")
    overdue_count = (not_done_dates < today_dt).sum()
    due_soon_count = ((not_done_dates >= today_dt) & (not_done_dates <= (today_dt + pd.Timedelta(days=7)))).sum()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Checklist Items", total_items)
    m2.metric("Done", done_count)
    m3.metric("Due Soon (Next 7 Days)", due_soon_count)
    m4.metric("Overdue", overdue_count)

    st.markdown("---")
    st.subheader("Interactive Plan Editor")
    st.caption("Allowed status values: `Not Started` | `In Progress` | `Done`")

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
                    "Semester Preparation",
                    "Assessments",
                    "Labs",
                    "Projects",
                    "Documents",
                    "Skills",
                    "Placement",
                ],
            ),
        },
        num_rows="dynamic",
        use_container_width=True,
        key="checklist_editor",
    )

    if st.button("💾 Save Plan & Checklist", type="primary"):
        clean_save = edited_checklist.loc[:, ~edited_checklist.columns.duplicated(keep="first")]
        clean_save.to_csv(os.path.join(DATA_DIR, "plan_checklist.csv"), index=False)
        st.success("✅ Changes saved to `data/plan_checklist.csv`!")
        st.rerun()

    st.markdown("---")
    st.subheader("Execution Focus Views")
    tab_week, tab_sem, tab_deg = st.tabs(["⚡ This Week (Due <= 7 Days)", "🎯 Semester Milestones", "🚀 Degree & Placement"])
    
    with tab_week:
        this_week = checklist_work[(checklist_work["p_date"] >= today_dt) & (checklist_work["p_date"] <= (today_dt + pd.Timedelta(days=7)))]
        st.dataframe(this_week[["category", "item", "target_date", "status", "notes"]], use_container_width=True)
    with tab_sem:
        cats = get_1d_series(checklist_work, "category", "")
        sem_tasks = checklist_work[cats.isin(["Semester Preparation", "Assessments", "Labs", "Projects"])]
        st.dataframe(sem_tasks[["category", "item", "target_date", "status", "notes"]], use_container_width=True)
    with tab_deg:
        cats = get_1d_series(checklist_work, "category", "")
        deg_tasks = checklist_work[cats.isin(["Documents", "Skills", "Placement"])]
        st.dataframe(deg_tasks[["category", "item", "target_date", "status", "notes"]], use_container_width=True)

# ==========================================
# TAB 10: ASK DEGREE AI (PHASE 6)
# ==========================================
elif selected_tab == "10. Ask Degree AI":
    st.title("🤖 Ask Degree AI")
    st.markdown("Ground-truth degree assistant answering strictly from your academic datasets.")

    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

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

    st.markdown("**Quick Questions:**")
    qc1, qc2, qc3, qc4, qc5 = st.columns(5)
    selected_prompt = None
    if qc1.button("Incomplete Courses Sem 3"):
        selected_prompt = "What courses are still incomplete in Semester 3?"
    if qc2.button("Next Internal Assessment"):
        selected_prompt = "When is my next internal assessment?"
    if qc3.button("Show Next Holiday"):
        selected_prompt = "Show my next holiday"
    if qc4.button("Data Structures Topics"):
        selected_prompt = "What topics are in Data Structures?"
    if qc5.button("Official CGPA Formula"):
        selected_prompt = "What is my official university CGPA formula?"

    user_query = st.text_input("Ask a question about your engineering degree:", value=selected_prompt or "")

    if user_query:
        query_norm = user_query.strip().lower()

        # Safe-AI Rule: Refuse unverified formulas and regulations
        unsupported_keywords = ["cgpa formula", "official formula", "exam regulation", "eligibility rule", "attendance policy"]
        is_unsupported = any(k in query_norm for k in unsupported_keywords)

        if is_unsupported:
            st.warning("⚠️ **Data Area Used:** None")
            st.error("I cannot verify that from the current Degree OS data.")
            st.caption("Safe-AI Rule: Institutional regulations and CGPA formulas are not inferred without an authoritative source document.")
        
        elif api_key and GEMINI_AVAILABLE:
            with st.spinner("Degree AI is reviewing academic datasets..."):
                try:
                    client = genai.Client(api_key=api_key)
                    sys_instruct = (
                        "You are Degree AI. Answer only from the supplied degree data. "
                        "Do not invent university rules, dates, marks, formulas or syllabus content. "
                        "If the requested information is missing, say: I cannot verify that from the current Degree OS data. "
                        "At the end of your answer, write exactly which data area was used: Courses, Calendar, Assessments, Scores, Plan, or None."
                    )
                    prompt_content = f"{context_data}\n\nStudent Question: {user_query}"
                    
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt_content,
                        config=types.GenerateContentConfig(
                            system_instruction=sys_instruct,
                            temperature=0.0,
                        )
                    )
                    st.markdown("### 💡 Degree AI Answer:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Gemini API query error ({e}). Falling back to local deterministic engine:")
                    api_key = ""

        if not api_key and not is_unsupported:
            st.markdown("### 💡 Degree AI Local Engine Answer:")

            # 1. Incomplete courses
            if "incomplete" in query_norm or ("courses" in query_norm and "semester 3" in query_norm):
                st.info("📌 **Data Area Used:** Courses")
                sem_series = get_1d_series(courses_df, "Semester", "")
                stat_series = get_1d_series(courses_df, "Status", "")
                sem3_incomplete = courses_df[(sem_series == "Semester 3") & (stat_series != "Completed")]
                if not sem3_incomplete.empty:
                    st.write("The following course(s) are incomplete in **Semester 3**:")
                    for _, r in sem3_incomplete.iterrows():
                        st.write(f"- **{r.get('Course Code')}**: {r.get('Course Title')} *(Status: {r.get('Status')})*")
                else:
                    st.write("All Semester 3 courses are marked as Completed.")

            # 2. Next assessment
            elif "assessment" in query_norm or "ia" in query_norm or "exam" in query_norm:
                st.info("📌 **Data Area Used:** Assessments")
                if not assessments_df.empty:
                    as_copy = assessments_df.copy()
                    as_copy["PDate"] = pd.to_datetime(get_1d_series(as_copy, "Date", ""), errors="coerce")
                    upcoming = as_copy[as_copy["PDate"] >= today_dt].sort_values("PDate")
                    if not upcoming.empty:
                        row = upcoming.iloc[0]
                        st.write(f"Your next assessment is **{row.get('Assessment Name')}** ({row.get('Course Code')}) scheduled on **{row.get('Date')}**.")
                    else:
                        st.write(f"Next recorded assessment: **{as_copy.iloc[0].get('Assessment Name')}** on **{as_copy.iloc[0].get('Date')}**.")
                else:
                    st.write("I cannot verify that from the current Degree OS data.")

            # 3. Next holiday
            elif "holiday" in query_norm or "leave" in query_norm or "break" in query_norm:
                st.info("📌 **Data Area Used:** Calendar")
                if not calendar_df.empty:
                    cal_copy = calendar_df.copy()
                    cal_copy["PDate"] = pd.to_datetime(get_1d_series(cal_copy, "Date", ""), errors="coerce")
                    types = get_1d_series(cal_copy, "Type", "").astype(str).str.lower()
                    leaves = cal_copy[types.str.contains("leave|holiday", na=False)]
                    upcoming_leaves = leaves[leaves["PDate"] >= today_dt].sort_values("PDate")
                    if not upcoming_leaves.empty:
                        row = upcoming_leaves.iloc[0]
                        st.write(f"Your next holiday is **{row.get('Event Title')}** on **{row.get('Date')}**.")
                    elif not leaves.empty:
                        st.write(f"Next holiday in calendar: **{leaves.iloc[0].get('Event Title')}** on **{leaves.iloc[0].get('Date')}**.")
                    else:
                        st.write("No upcoming holidays found in the calendar.")
                else:
                    st.write("I cannot verify that from the current Degree OS data.")

            # 4. Course syllabus topics
            elif "data structures" in query_norm or "syllabus" in query_norm or "topics" in query_norm:
                st.info("📌 **Data Area Used:** Courses")
                title_series = get_1d_series(courses_df, "Course Title", "").astype(str)
                ds_course = courses_df[title_series.str.contains("Data Structures", case=False, na=False)]
                if not ds_course.empty:
                    topics = ds_course.iloc[0].get("Syllabus Topics", "N/A")
                    st.write(f"Topics in **Data Structures ({ds_course.iloc[0].get('Course Code')})**:")
                    st.markdown(f"> {topics}")
                else:
                    st.write("I cannot verify that from the current Degree OS data.")

            # 5. Checklist status
            elif "checklist" in query_norm or "task" in query_norm or "plan" in query_norm:
                st.info("📌 **Data Area Used:** Plan")
                st.write(f"Checklist Summary: {len(checklist_df)} total tasks recorded. Pending tasks:")
                stat_col = get_1d_series(checklist_df, "status", "").astype(str).str.lower()
                pending = checklist_df[stat_col != "done"]
                for _, r in pending.iterrows():
                    st.write(f"- [{r.get('status')}] **{r.get('item')}** (Target: {r.get('target_date')})")

            # 6. Semester status
            elif "semester" in query_norm:
                st.info("📌 **Data Area Used:** Semesters")
                st.dataframe(semesters_df[["Semester", "Status", "Completed Credits", "Target Credits"]], use_container_width=True)

            else:
                st.warning("📌 **Data Area Used:** None")
                st.write("I cannot verify that from the current Degree OS data.")

# ==========================================
# TAB 11: DATA ADMIN (PHASE 7)
# ==========================================
elif selected_tab == "11. Data Admin":
    st.title("🛠️ Data Administrator")
    st.markdown("Directly edit, update, or reset any dataset to test data maintainability.")

    table_options = {
        "semesters.csv": (semesters_df, DEFAULT_SEMESTERS),
        "courses.csv": (courses_df, DEFAULT_COURSES),
        "university_syllabus.csv": (univ_syllabus_df, DEFAULT_UNIV_SYLLABUS),
        calendar_filename: (calendar_df, DEFAULT_CALENDAR),
        "assessments.csv": (assessments_df, DEFAULT_ASSESSMENTS),
        "scores.csv": (scores_df, DEFAULT_SCORES),
        "plan_checklist.csv": (checklist_df, DEFAULT_CHECKLIST),
    }

    choice = st.selectbox("Select Dataset to Edit", list(table_options.keys()))
    df_to_edit, default_blueprint = table_options[choice]

    st.markdown(f"Editing **`{choice}`**:")
    edited_data = st.data_editor(df_to_edit, num_rows="dynamic", use_container_width=True, key=f"admin_editor_{choice}")

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("💾 Save Changes", type="primary"):
            clean_edited = edited_data.loc[:, ~edited_data.columns.duplicated(keep="first")]
            clean_edited.to_csv(os.path.join(DATA_DIR, choice), index=False)
            st.success(f"✅ Successfully updated and saved `{choice}`!")
            st.rerun()
    with col_btn2:
        if st.button(f"🔄 Reset `{choice}` to Blueprint Template"):
            default_blueprint.to_csv(os.path.join(DATA_DIR, choice), index=False)
            st.warning(f"Reset `{choice}` to clean template!")
            st.rerun()


