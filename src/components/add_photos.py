import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

from PIL import Image

@st.dialog("Capture or uplode photo")

def add_attendance_photos_dialog():
    st.write("Add classroom photos for attendance. You can either capture a photo using your cam or upload an existing photo from your device.")


    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab='camera'

    t1,t2=st.columns([1,1])

    with t1:
        if st.button('Camera',key='camera_tab_button',width='stretch'):
            st.session_state.photo_tab='camera'

    with t2:
        if st.button('Upload',key='upload_tab_button',width='stretch'):
            st.session_state.photo_tab='upload'

    if st.session_state.photo_tab=='camera':
        cam_photo=st.camera_input("Capture a photo",key='attendance_camera_input')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo added successfully.",icon="✅")
            st.rerun()

    if st.session_state.photo_tab=='upload':
        upload_photo=st.file_uploader("Upload a photo",type=['jpg','jpeg','png'],key='attendance_upload_input',accept_multiple_files=True)
        if upload_photo:
            for f in upload_photo:
                st.session_state.attendance_images.append(Image.open(f))
            
            st.toast("Photo added successfully.",icon="✅")
            st.rerun()

    st.divider()
    if st.button("Done",key='attendance_photos_done_button',width='stretch'):
        
        st.rerun()