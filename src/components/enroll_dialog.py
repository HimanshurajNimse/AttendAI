import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write(
        "Enter the subject code provided by your teacher to enroll in the subject."
    )

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )

    if st.button("Enroll now", width="stretch"):

        if not join_code:
            st.warning("Please enter a subject code.")
            return

        # Find the subject using the subject code
        res = (
            supabase
            .table("subjects")
            .select("subject_id, name, subject_code")
            .eq("subject_code", join_code)
            .execute()
        )

        if not res.data:
            st.error("Invalid subject code.")
            return

        # Get subject information
        subject = res.data[0]

        subject_id = subject["subject_id"]
        subject_name = subject["name"]
        subject_code = subject["subject_code"]

        # Get current student
        student_id = st.session_state.student_data["student_id"]

        # Check if already enrolled
        check = (
            supabase
            .table("subject_student")
            .select("*")
            .eq("subject_id", subject_id)
            .eq("student_id", student_id)
            .execute()
        )

        if check.data:

            st.error("You are already enrolled in this subject.")

        else:

            # Enroll student
            enroll_student_to_subject(
                student_id,
                subject_id
            )

            st.success(
                f"You have successfully enrolled in "
                f"{subject_name} ({subject_code})."
            )

            time.sleep(1)
            st.rerun()