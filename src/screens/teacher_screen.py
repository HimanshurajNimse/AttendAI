import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime
import pandas as pd

from src.UI.base_layout import background,base_style_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dash

from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_subjects_by_teacher,get_attendance_for_teacher
from src.database.config import supabase
from src.components.create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_subject_code import share_subject_code
from src.components.add_photos import add_attendance_photos_dialog
from src.components.attendance_result import attendance_result_dialog
from src.components.voice_attendance import voice_attendance_dialog

from src.pipeline.face_pipeline import predict_attendance

def teacher_screen():
    #header_dashboard()
    
    base_style_layout()


    
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()

    

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data

    
    c1,c2=st.columns(2,vertical_alignment='center',gap='large')
        
    
    with c1:
        header_dashboard()
    
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']}""")
        if st.button("Logout",key='loginbackbutton'):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()

    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='Take Attendance'
    tab1,tab2,tab3=st.columns(3)

    with tab1:
        if st.button('Take Attendance',icon=':material/assignment_turned_in:',width='stretch'  ):
            st.session_state.current_teacher_tab='Take Attendance'
            st.rerun()

    with tab2:
        if st.button('Manage Subjects',icon=':material/book_ribbon:',width='stretch'  ):
            st.session_state.current_teacher_tab='Manage Subjects'
            st.rerun()

    with tab3:
        if st.button('View Attendance Records',icon=':material/cards_stack:',width='stretch'  ):
            st.session_state.current_teacher_tab='Attendance Records'
            st.rerun()

    st.divider()


    if st.session_state.current_teacher_tab=='Take Attendance':
        teacher_take_attendance()

    if st.session_state.current_teacher_tab=='Manage Subjects':
        teacher_manage_subjects()

    if st.session_state.current_teacher_tab=='Attendance Records':
        teacher_view_attendance_records()

    
    footer_dash()



def teacher_take_attendance():
    teacher_id=st.session_state.teacher_data['teacher_id']

    st.markdown(
            """
            <h2 style="text-align:center;">
                Take Attendance
            </h2>
            """,
            unsafe_allow_html=True
        )
    #st.info("This feature is under development. Please check back later.", icon="ℹ️")


    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images=[]
    subjects=get_subjects_by_teacher(teacher_id)

    if not subjects:
        st.info("No subjects found. Please add a subject to get started.", icon="ℹ️") 
        return

    subject_options={f"{sub['name']} ({sub['subject_code']})":sub['subject_id'] for sub in subjects}

    col1,col2=st.columns([3,1],vertical_alignment='bottom')
    with col1:
        select_subject_label=st.selectbox("Select Subject",options=list(subject_options.keys()),key='attendance_subject_select')

    with col2:
        if st.button('Add photos',icon=':material/add_a_photo:',width='stretch',key='add_attendance_photos_button'):
            add_attendance_photos_dialog()

    selected_subject_id=subject_options[select_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.markdown(
            """
            <h2 style="text-align:center;">
                Added Photos
            </h2>
            """,
            unsafe_allow_html=True
        )
        gallery_col=st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_col[idx%4]:
                st.image(img,width="stretch",caption=f"Photo {idx+1}")

    c1,c2,c3=st.columns(3)

    with c1:
        if st.button("Clear all photos",width='stretch',icon=':material/delete:'):
            st.session_state.attendance_images=[]
            st.rerun

    with c2:
        has_photos=bool(st.session_state.attendance_images)
        if st.button('Run Face Analysis', width='stretch',icon=':material/analytics:',disabled=not has_photos):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_id={}

                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np=np.array(img.convert('RGB'))

                    detected,_,_=predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id=int(sid)

                            all_detected_id.setdefault(student_id,[]).append(f"Photos {idx+1}")

                    enrolled_res = (
                        supabase
                        .table('subject_student')
                        .select("*,students(*)")
                        .eq(
                            'subject_id',
                            selected_subject_id
                        )
                        .execute()
                    )
                    enrolled_students=enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    results,attendance_to_log=[],[]

                    current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student=node['students']
                        sources=all_detected_id.get(int(student['student_id']),[])

                        is_present=len(sources)>0

                        results.append({
                            "Name":student['name'],
                            "ID":student['student_id'],
                            "Source": ",".join(sources) if is_present else "-",
                            "Status":"✅ Present" if is_present else "❎ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id':selected_subject_id,
                            'timestamp':current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results),attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance',width='stretch',icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)
            
                    








        
def teacher_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h2 style="text-align:center;">
                Manage Subjects
            </h2>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if st.button(
            "Add Subject",
            key='addsubjectbutton',
            width='content'
        ):
            create_subject_dialog(teacher_id)

    # LIST ALL SUBJECTS
    subjects = get_subjects_by_teacher(teacher_id)

    if subjects:

        for sub in subjects:

            stats = [
                ("👥", "Total Students", sub['total_students']),
                ("📅", "Total Sessions", sub['total_sessions']),
            ]

            def share_btn(
                subject_name=sub['name'],
                subject_code=sub['subject_code']
            ):
                if st.button(
                    f"Share Code: {subject_name}",
                    key=f"share_{subject_code}",
                    icon=":material/share:",
                    use_container_width=True
                ):
                    share_subject_code(
                        subject_name,
                        subject_code
                    )

                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info(
            "No subjects found. Please add a subject to get started.",
            icon="ℹ️"
        )

def teacher_view_attendance_records():
    st.markdown(
        """
        <h2 style="text-align:center;">
            View Attendance Records
        </h2>
        """,
        unsafe_allow_html=True
    )

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found.")
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        if not ts:
            continue

        # Convert timestamp to a consistent datetime
        dt = pd.to_datetime(ts)

        data.append({
            "Session": dt,
            "Time": dt.strftime("%Y-%m-%d %I:%M %p"),
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    if not data:
        st.info("No valid attendance records found.")
        return

    df = pd.DataFrame(data)

    # Group attendance records belonging to the same session
    summary = (
        df.groupby(
            ['Session', 'Time', 'Subject', 'Subject Code'],
            as_index=False
        )
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
    )

    # Create attendance display text
    summary['Attendance Stats'] = (
        "✅ "
        + summary['Present_Count'].astype(str)
        + "/"
        + summary['Total_Count'].astype(str)
        + " Students"
    )

    # Sort newest sessions first
    display_df = (
        summary
        .sort_values(
            by='Session',
            ascending=False
        )
        [
            [
                'Time',
                'Subject',
                'Subject Code',
                'Attendance Stats'
            ]
        ]
    )

    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True
    )




def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)

    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False

def teacher_screen_login():
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
            Login using Password
        </h2>
        """,
        unsafe_allow_html=True
    )
    
    st.space()
    

    teacher_username=st.text_input("Enter Username:", placeholder='enter your username')
    teacher_pass=st.text_input("Enter Password:",type='password', placeholder='enter password')

    st.divider()
    login_failed=False

    btc1,btc2=st.columns(2)

    with btc1:
        if st.button('Login',icon=':material/passkey:',width='stretch'):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Welcome back!",icon="👋🏻")
                import time
                time.sleep(3)
                st.rerun()
            else:
                login_failed=True


    with btc2:
        if st.button("Register Instead",
            icon=":material/person_add:",
            use_container_width=True):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    if login_failed:
        st.error(
            "Invalid username and password combination",
            width="stretch",
        )
    footer_dash()
    
    
def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False,"All fields are required"
    if check_teacher_exists(teacher_username):
        return False,"Username Already taken"
    if teacher_pass!=teacher_pass_confirm:
        return False,"password doesnt match"

    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Successfully created! Login Now"
    except Exception as e:
        return False,str(e)
    
def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='large')
    
    base_style_layout()

    with c1:
        header_dashboard()

    with c2:
        if st.button("Home",key='loginbackbutton'):
            st.session_state['login_type']=None
            st.rerun()

        
        
    st.markdown(
        """
        <h2 style="text-align:center;">
            Register your Teacher Profile
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.space()
        
    
    teacher_username=st.text_input("Enter Username:", placeholder='create username')
    teacher_name=st.text_input("Enter name:", placeholder='enter your name')
    teacher_pass=st.text_input("Enter Password:",type='password', placeholder='enter password')
    teacher_pass_confirm=st.text_input("Confirm your Password:",type='password', placeholder='confirm your password')
    
    st.divider()
    error_message=None
    success_message=None
    
    btc1,btc2=st.columns(2)
    
    with btc1:
        if st.button("Login Instead",icon=":material/person_add:",
                    use_container_width=True):
            st.session_state.teacher_login_type = "login"
            st.rerun()
    with btc2:
        if st.button('Register',icon=':material/passkey:',width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                success_message=message
            else:
                error_message = message
    
    if success_message:
        st.success(success_message, width="stretch")
        import time
        time.sleep(2)
        st.session_state.teacher_login_type = "login"
        st.rerun()    
    if error_message:
        st.error(error_message, width="stretch")
    footer_dash()