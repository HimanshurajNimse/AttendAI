import streamlit as st
from PIL import Image
import numpy as np

import os

from src.UI.base_layout import background,base_style_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dash

from src.pipeline.face_pipeline import predict_attendance,get_face_embeddings,train_classifier
from src.pipeline.voice_pipeline import get_voice_embedding

from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance_logs
from src.components.enroll_dialog import enroll_dialog
from src.components.subject_card import subject_card



def student_dashboard():
    
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", key="loginbackbutton"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.session_state["login_type"] = None
            st.rerun()

    st.space()

    c1,c2=st.columns(2)

    with c1:
        st.markdown(
            """
                    <h2 style="text-align:center;">
                        Your Enrolled Subjects
                    </h2>
                    """,
                    unsafe_allow_html=True
        )
    with c2:
        if st.button("Enroll in Subject",width='stretch'):
            enroll_dialog()

    st.divider()


    with st.spinner('Fetching your subjects...'):
        subject = get_student_subjects(student_id)
        logs= get_student_attendance_logs(student_id)


    stats_map={}

    for log in logs:
        sid=log['subject_id']
        if sid not in stats_map:
            stats_map[sid]={'total_sessions':0,'present_count':0}
        stats_map[sid]['total_sessions']+=1

        if log['status']=='present':
            stats_map[sid]['present_count']+=1

    cols=st.columns(2)

    for i ,sub_node in enumerate(subject):
        sub=sub_node['subjects']
        sid=sub['subject_id']

        stats=stats_map.get(sid,{'total_sessions':0,'present_count':0})
        def unenroll_btn():
                if st.button('Unenroll from this course',key=f'unenroll_{sid}',width='stretch'):
                    from src.database.db import unenroll_student_from_subject
                    unenroll_student_from_subject(student_id,sid)
                    st.toast(f"You have successfully unenrolled from {sub['name']} ({sub['subject_code']}).")
                    import time
                    time.sleep(1)
                    st.rerun()
        

        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("🗓️",'Total',stats['total_sessions']),
                    ("✅",'Present',stats['present_count']),
                    ("❌",'Absent',stats['total_sessions']-stats['present_count'])
                ],
                footer_callback=unenroll_btn
            )
    footer_dash()

def student_screen():
    base_style_layout()

    if st.session_state.get("student_data") is not None:
        student_dashboard()
        return

    
    c1,c2=st.columns(2,vertical_alignment='center',gap='large')
    

    with c1:
        header_dashboard()

    with c2:
        if st.button("Home",key='loginbackbutton'):
            st.session_state['login_type']=None
            st.rerun()
    st.markdown(
        """
        <h2 style="text-align:center;">
            Login using face id
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.space()

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    photo_src=st.camera_input("Position your face in center")
    if photo_src:
        img=np.array(Image.open(photo_src))


        with st.spinner('AI is scanning..'):
            detected,all_ids,num_face=predict_attendance(img)

            if num_face == 0:
                st.warning('face not found! Position your face properly')
                #st.session_state.show_registration = True
            elif num_face>1:
                st.warning('Multiple faces found!')

            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()
                    student=next((s for s in all_students if s['student_id']==student_id),None)

                    if student:
                        st.session_state.login_type = "student"
                        st.session_state.is_logged_in=True
                        st.session_state.user_role='student'
                        st.session_state.student_data=student
                        st.toast(f"Welcome Back {student['name']}")
                        import time
                        time.sleep(2)
                        st.rerun()

                else:
                    st.info('Face not recognized! You might be a new student!')
                    st.session_state.show_registration = True


    if st.session_state.show_registration:
        with st.container(border=True):
            st.markdown(
                    """
                    <h2 style="text-align:center;">
                        Register new Profile!
                    </h2>
                    """,
                    unsafe_allow_html=True
                )
            new_name=st.text_input("Enter Your Name", placeholder='E.g. Himan Nimse')

            st.markdown(
                    """
                    <h3 style="text-align:center;">
                        Optional: Voice Enrollment
                    </h3>
                    """,
                    unsafe_allow_html=True
                )
            st.info('enroll your voice for voice only attendance ')

            audio_data=None

            try:
                audio_data=st.audio_input("Record a short phrase like I am present, My name is Anushka.")
            except Exception:
                st.error('Audio Data Failed!')

            if st.button('Create Account'):
                if new_name:
                    with st.spinner('Creating profile...'):
                        image=np.array(Image.open(photo_src))
                        encodings=get_face_embeddings(image)
                        if encodings:
                            face_emb=encodings[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())
                            response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()

                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f"Profile created. Hiii {new_name}!")
                                import time
                                time.sleep(2)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration!')
                else:
                    st.warning('Please enter your name!')

            




    st.space()
    footer_dash()