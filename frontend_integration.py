# FRONTEND INTEGRATION GUIDE
# Apply these changes to your existing app.py; do not replace your UI pages.

# A) At the top of app.py, after imports:
from dotenv import load_dotenv
load_dotenv()

from backend import get_backend, show_authentication, logout_button

# B) After your DEFAULT_* DataFrames are defined, but BEFORE loading data:
if not show_authentication():
    st.stop()

backend = get_backend()
logout_button()

# C) Replace your current seven CSV load calls:
semesters_df = backend.load_dataframe("semesters", DEFAULT_SEMESTERS)
courses_df = backend.load_dataframe("courses", DEFAULT_COURSES)
univ_syllabus_df = backend.load_dataframe("university_syllabus", DEFAULT_UNIV_SYLLABUS)

# Preserve your current filename choice if you still use it for display,
# but the cloud dataset name is always "calendar".
calendar_df = backend.load_dataframe("calendar", DEFAULT_CALENDAR)

assessments_df = backend.load_dataframe("assessments", DEFAULT_ASSESSMENTS)
scores_df = backend.load_dataframe("scores", DEFAULT_SCORES)
checklist_df = backend.load_dataframe("plan_checklist", DEFAULT_CHECKLIST)

# Remove/skip the old load_data_file(...) calls for these datasets.
# Keep your get_1d_series helper and all UI page code.

# D) In Plan & Checklist, replace the CSV save block:
#
# OLD:
# clean_save.to_csv(os.path.join(DATA_DIR, "plan_checklist.csv"), index=False)
#
# NEW:
# backend.save_dataframe("plan_checklist", clean_save)
# st.success("Changes saved to your Supabase account!")
# st.rerun()

# E) In Data Admin, replace the save block:
#
# OLD:
# clean_edited.to_csv(os.path.join(DATA_DIR, choice), index=False)
#
# NEW:
# dataset_name = {
#     "semesters.csv": "semesters",
#     "courses.csv": "courses",
#     "university_syllabus.csv": "university_syllabus",
#     "academic_calendar.csv": "calendar",
#     "calendar.csv": "calendar",
#     "assessments.csv": "assessments",
#     "scores.csv": "scores",
#     "plan_checklist.csv": "plan_checklist",
# }[choice]
# backend.save_dataframe(dataset_name, clean_edited)
# st.success(f"Successfully updated {choice} in Supabase!")
# st.rerun()

# F) In Data Admin, replace the reset-to-blueprint CSV write:
#
# OLD:
# default_blueprint.to_csv(os.path.join(DATA_DIR, choice), index=False)
#
# NEW:
# backend.save_dataframe(dataset_name, default_blueprint)
# st.warning(f"Reset {choice} to its default template in Supabase!")
# st.rerun()

# G) Important: The Data Admin table_options keys must map to cloud dataset names
# as shown in section E. The frontend can still keep its current labels/CSV names.
