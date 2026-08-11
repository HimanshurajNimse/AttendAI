import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data["student_id"]

    res=supabase.table("subjects").select("subject_id, name, subject_code").eq("subject_code",subject_code).execute()
    if not res.data:
        st.error("Invalid subject code.")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return
    subject=res.data[0]
    check=supabase.table("subject_student").select("*").eq("subject_id",subject['subject_id']).eq("student_id",student_id).execute()
    if check.data:
        st.info(f"You are already enrolled in {subject['name']} ({subject['subject_code']}).")
        if st.button("Got it"):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"Do you want to enroll in **{subject['name']} ({subject['subject_code']})**?")
    col1,col2=st.columns(2)
    with col1:
        if st.button('No Thanks'):
            st.query_params.clear()
            st.rerun()
        
    with col2:
        if st.button("Enroll Now",width='stretch'):
            enroll_student_to_subject(student_id,subject['subject_id'])
            st.success(f"You have successfully enrolled in {subject['name']} ({subject['subject_code']}).")
            
            st.query_params.clear()
            time.sleep(1)
            st.rerun()