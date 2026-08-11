from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())

def check_teacher_exists(username):
    response=supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0


def create_teacher(username,password,name):
    data={"username":username,"password_hash":hash_pass(password),"name":name}

    response=supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username,password):
    response=supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher['password_hash']):
            return teacher

    return None

def get_all_students():
    response=supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name,face_embedding=None,voice_embedding=None):
    data={'name': new_name,'face_embedding':face_embedding,'voice_embedding':voice_embedding}
    response=supabase.table('students').insert(data).execute()
    return response.data

def create_subject(teacher_id,sub_id,sub_name,sub_section):
    data={'teacher_id':teacher_id,'subject_code':sub_id,"name": sub_name,'section':sub_section}
    response=supabase.table('subjects').insert(data).execute()
    return response.data

def get_subjects_by_teacher(teacher_id):
    response = (
        supabase
        .table('subjects')
        .select("*,subject_student(count)")
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:

        # -----------------------------
        # Total students
        # -----------------------------
        subject_students = sub.get('subject_student', [])

        if subject_students:
            sub['total_students'] = subject_students[0].get(
                'count',
                0
            )
        else:
            sub['total_students'] = 0

        # -----------------------------
        # Get attendance sessions
        # -----------------------------
        attendance_response = (
            supabase
            .table('attendance_logs')
            .select('timestamp')
            .eq('subject_id', sub['subject_id'])
            .execute()
        )

        attendance_logs = attendance_response.data or []

        # One unique timestamp = one attendance session
        unique_sessions = set(
            log['timestamp']
            for log in attendance_logs
            if log.get('timestamp')
        )

        sub['total_sessions'] = len(unique_sessions)

        # Remove nested student data
        sub.pop('subject_student', None)

    return subjects


def enroll_student_to_subject(student_id,subject_id):
    data={'student_id':student_id,'subject_id':subject_id}
    response=supabase.table('subject_student').insert(data).execute()
    return response.data

def unenroll_student_from_subject(student_id,subject_id):
    response=supabase.table('subject_student').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response=supabase.table('subject_student').select("*,subjects(*)").eq('student_id',student_id).execute()
    return response.data

def get_student_attendance_logs(student_id):
    response = (
        supabase
        .table('attendance_logs')
        .select("*")
        .eq('student_id', student_id)
        .execute()
    )

    logs = response.data

    for log in logs:
        log['status'] = 'present' if log.get('is_present', False) else 'absent'

    return logs

def create_attendance(logs):
    response=supabase.table('attendance_logs').insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response=supabase.table('attendance_logs').select("*,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data
    
