import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.UI.base_layout import base_style_layout,background

def home_screen():
    
    base_style_layout()
    background()

    header_home()
    col1,col2=st.columns(2,gap='large')

    with col1:
            st.markdown("<h2 style='text-align:center;'>I AM TEACHER</h2>", unsafe_allow_html=True)
            st.image("https://i.ibb.co/pv7Vh3Wj/Chat-GPT-Image-Jul-21-2026-01-53-43-PM.png",width=180)
            if st.button('Teacher Portal',icon=':material/arrow_outward:',use_container_width=True):
                st.session_state['login_type']='teacher'
                st.rerun()

    with col2:
        
        st.markdown("<h2 style='text-align:center;'>I AM STUDENT</h2>", unsafe_allow_html=True)
        st.image("https://i.ibb.co/rKWTHJPP/student.png",width=180)
        if st.button('Student Portal',icon=':material/arrow_outward:',use_container_width=True):
            st.session_state['login_type']='student'
            st.rerun()

    footer_home()
