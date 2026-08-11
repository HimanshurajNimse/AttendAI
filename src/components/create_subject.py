import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject below:")
    sub_id=st.text_input("Subject Code",placeholder="CSE-101")
    sub_name=st.text_input("Subject Name",placeholder="Computer Science")
    sub_section=st.text_input("Section",placeholder="A")

    if st.button("Create Subject Now",width='content'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(teacher_id,sub_id,sub_name,sub_section)
                st.toast(f"Subject {sub_name} created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {str(e)}")

        else:
            st.error("Please fill in all the fields before creating the subject.")