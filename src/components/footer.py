import streamlit as st

def footer_home():
    st.markdown("""
    <hr style="margin-top:40px; border:1px solid rgba(255,255,255,.08);">

    <p style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        color:#94A3B8;
        font-size:15px;
        font-family:'Outfit',sans-serif;
        margin:0;
    ">
        <span>© 2026 <b style="color:#E0E3FF;">AttendAI</b>. All Rights Reserved.</span>
        <span>Made by <b style="color:#4F8CFF;">Himanshuraj Nimse</b></span>
    </p>
    """, unsafe_allow_html=True)

def footer_dash():
    st.markdown("""
        <hr style="margin-top:40px; border:1px solid rgba(255,255,255,.08);">
    
        <p style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            color:#94A3B8;
            font-size:15px;
            font-family:'Outfit',sans-serif;
            margin:0;
        ">
            <span>© 2026 <b style="color:#E0E3FF;">AttendAI</b>. All Rights Reserved.</span>
            <span>Made by <b style="color:#4F8CFF;">Himanshuraj Nimse</b></span>
        </p>
        """, unsafe_allow_html=True)