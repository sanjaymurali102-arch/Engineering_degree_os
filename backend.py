
"""Supabase backend for My Engineering Degree OS.

Uses the Supabase publishable key (or legacy anon key)
and the authenticated user's JWT.
Never put the database password in frontend code.
"""

import os
from typing import Any

import pandas as pd
import streamlit as st
from supabase import Client, create_client


DATASETS = {
    "semesters": "semesters",
    "courses": "courses",
    "university_syllabus": "university_syllabus",
    "calendar": "calendar",
    "assessments": "assessments",
    "scores": "scores",
    "plan_checklist": "plan_checklist",
}


class BackendConfigError(RuntimeError):
    pass


class SupabaseBackend:

    def __init__(self, client: Client):
        self.client = client

    @classmethod
    def from_env(cls) -> "SupabaseBackend":

        url = os.getenv("SUPABASE_URL", "").strip()

        key = (
            os.getenv("SUPABASE_PUBLISHABLE_KEY", "").strip()
            or os.getenv("SUPABASE_ANON_KEY", "").strip()
        )

        if not url or not key:
            raise BackendConfigError(
                "Set SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY "
                "in your environment."
            )

        return cls(create_client(url, key))

    # ---------------- AUTHENTICATION ----------------

    def sign_up(self, email: str, password: str):
        return self.client.auth.sign_up({
            "email": email,
            "password": password
        })

    def sign_in(self, email: str, password: str):
        return self.client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

    def sign_out(self):
        self.client.auth.sign_out()

    def current_user(self):
        return self.client.auth.get_user()

    def _require_user_id(self) -> str:

        result = self.current_user()
        user = getattr(result, "user", None)

        if user is None or not getattr(user, "id", None):
            raise PermissionError(
                "Please sign in before accessing your academic data."
            )

        return str(user.id)

    # ---------------- LOAD DATA ----------------

    def load_dataframe(
        self,
        dataset: str,
        default_df: pd.DataFrame
    ) -> pd.DataFrame:

        if dataset not in DATASETS:
            raise ValueError(f"Unknown dataset: {dataset}")

        user_id = self._require_user_id()

        response = (
            self.client.table("degree_records")
            .select("row_data, position")
            .eq("user_id", user_id)
            .eq("dataset", dataset)
            .order("position")
            .execute()
        )

        rows = response.data or []

        if not rows:
            self.save_dataframe(dataset, default_df)
            return default_df.copy()

        records = [row.get("row_data", {}) for row in rows]

        df = pd.DataFrame(records)

        for col in default_df.columns:
            if col not in df.columns:
                df[col] = pd.Series(dtype=default_df[col].dtype)

        ordered = (
            list(default_df.columns)
            + [c for c in df.columns if c not in default_df.columns]
        )

        return df.reindex(columns=ordered)

    # ---------------- SAVE DATA ----------------

    def save_dataframe(
        self,
        dataset: str,
        dataframe: pd.DataFrame
    ) -> None:

        if dataset not in DATASETS:
            raise ValueError(f"Unknown dataset: {dataset}")

        user_id = self._require_user_id()

        clean = dataframe.copy()
        clean = clean.astype(object).where(pd.notna(clean), None)

        records = []

        for index, row in enumerate(clean.to_dict(orient="records")):

            records.append({
                "user_id": user_id,
                "dataset": dataset,
                "position": index,
                "row_data": _json_safe(row),
            })

        # Remove previous rows for this user and dataset.
        (
            self.client.table("degree_records")
            .delete()
            .eq("user_id", user_id)
            .eq("dataset", dataset)
            .execute()
        )

        # Insert updated rows in batches.
        if records:
            for start in range(0, len(records), 500):

                (
                    self.client.table("degree_records")
                    .insert(records[start:start + 500])
                    .execute()
                )

    # ---------------- DELETE DATA ----------------

    def delete_dataset(self, dataset: str) -> None:

        if dataset not in DATASETS:
            raise ValueError(f"Unknown dataset: {dataset}")

        user_id = self._require_user_id()

        (
            self.client.table("degree_records")
            .delete()
            .eq("user_id", user_id)
            .eq("dataset", dataset)
            .execute()
        )


# ---------------- JSON CONVERSION ----------------

def _json_safe(value: Any) -> Any:

    if value is None:
        return None

    if hasattr(value, "to_pydatetime"):
        return value.to_pydatetime().isoformat()

    if hasattr(value, "isoformat") and not isinstance(value, str):
        try:
            return value.isoformat()
        except Exception:
            pass

    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass

    if value is None:
        return None

    if isinstance(value, dict):
        return {
            str(k): _json_safe(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]

    if isinstance(value, (str, int, float, bool)):
        return value

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    return str(value)


# ---------------- BACKEND INSTANCE ----------------

def get_backend() -> SupabaseBackend:

    if "_degree_supabase_backend" not in st.session_state:

        st.session_state["_degree_supabase_backend"] = (
            SupabaseBackend.from_env()
        )

    return st.session_state["_degree_supabase_backend"]


# ---------------- LOGIN / REGISTRATION ----------------

def show_authentication() -> bool:

    if st.session_state.get("degree_user_authenticated", False):
        return True

    try:
        backend = get_backend()

    except BackendConfigError as exc:
        st.error(str(exc))
        st.info(
            "Create a .env file from .env.example "
            "and restart Streamlit."
        )
        return False

    st.title("🎓 My Engineering Degree OS")
    st.subheader("Sign in to your academic workspace")

    mode = st.radio(
        "Account",
        ["Login", "Create account"],
        horizontal=True
    )

    with st.form("degree_auth_form"):

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Login" if mode == "Login" else "Create account",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not email.strip() or not password:

            st.warning("Enter both your email and password.")

        else:

            try:

                if mode == "Login":

                    result = backend.sign_in(
                        email.strip(),
                        password
                    )

                else:

                    result = backend.sign_up(
                        email.strip(),
                        password
                    )

                user = getattr(result, "user", None)
                session = getattr(result, "session", None)

                if user and session:

                    st.session_state["degree_user_authenticated"] = True
                    st.session_state["degree_user_email"] = email.strip()

                    st.success("Authentication successful!")
                    st.rerun()

                elif user and mode == "Create account":

                    st.success(
                        "Account created! Please confirm your email "
                        "if email verification is enabled, then log in."
                    )

                else:

                    st.error(
                        "Authentication did not return an active session. "
                        "Check your Supabase Auth settings."
                    )

            except Exception as exc:

                error_message = str(exc).lower()

                if "invalid login credentials" in error_message:

                    st.error(
                        "❌ Incorrect email or password. Please try again."
                    )

                elif "email not confirmed" in error_message:

                    st.warning(
                        "⚠️ Please verify your email first."
                    )

                elif "already registered" in error_message:

                    st.warning(
                        "This email is already registered. Please log in."
                    )

                else:

                    st.error(
                        f"❌ Authentication failed: {exc}"
                    )

    return False


# ---------------- LOGOUT ----------------

def logout_button():

    if st.sidebar.button(
        "🚪 Sign out",
        use_container_width=True
    ):

        try:
            get_backend().sign_out()

        except Exception as exc:
            st.warning(f"Sign-out warning: {exc}")

        finally:

            st.session_state.pop(
                "degree_user_authenticated",
                None
            )

            st.session_state.pop(
                "degree_user_email",
                None
            )

            st.rerun()
