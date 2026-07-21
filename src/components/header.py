import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/pjfJkNJc/logo.png"

    st.markdown(
        f"""
        <div style="display:flex;  align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px;">
            <img src="{logo_url}" style="height:100px;" alt="AttendAI Logo">
            <h1 style="text-align:center; color:#E0E3FF;">Attend AI</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )