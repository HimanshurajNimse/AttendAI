# AttendAI 🎓

**Attendance, reimagined.** AttendAI is a Streamlit web app that automates classroom attendance using **face recognition** and **voice recognition**, backed by a Supabase database.

![AttendAI Screenshot](streamlit_capture.jpg)

## Features

- **Two portals** — separate flows for **Teachers** and **Students** from a single home screen.
- **Face-ID login & self-registration** — students log in with their camera; unrecognized faces trigger an on-the-spot profile registration flow.
- **Photo-based attendance** — teachers upload one or more classroom photos, AttendAI detects and matches every face against enrolled students, and marks them present/absent automatically.
- **Voice attendance** — teachers can instead record classroom audio; AttendAI splits it into speech segments and matches each voice against enrolled students' voiceprints.
- **Subject management** — teachers create subjects, view enrollment/session stats, and share a join link or auto-generated **QR code** for students to enroll.
- **Auto-enroll via link** — students who open a shared join link (`?join=<subject_code>`) are prompted to enroll automatically.
- **Attendance records & history** — per-subject session summaries for teachers, and per-subject present/absent stats for students.
- **Secure teacher accounts** — username/password auth with bcrypt password hashing.

## How It Works

| Pipeline | Approach |
|---|---|
| **Face recognition** | OpenCV Haar Cascade for face detection → `dlib` face recognition model for 128-d embeddings → SVM classifier (`scikit-learn`) trained on enrolled students, with a Euclidean-distance confidence threshold. |
| **Voice recognition** | `librosa` for audio loading/segmentation → `resemblyzer` voice encoder for speaker embeddings → cosine-similarity matching against enrolled voiceprints. |
| **Data & auth** | Supabase (Postgres) stores teachers, students, subjects, enrollments, and attendance logs; `bcrypt` hashes teacher passwords. |
| **QR / sharing** | `segno` generates a QR code for each subject's join link. |

## Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io/)
- **Computer Vision**: OpenCV, dlib, `face_recognition_models`
- **Machine Learning**: scikit-learn (SVM classifier)
- **Voice Recognition**: librosa, resemblyzer
- **Database**: Supabase
- **Other**: Pillow, NumPy, Pandas, bcrypt, segno

## Project Structure

```
AttendAI/
├── app.py                     # App entry point & routing
├── requirements.txt
├── streamlit_capture.jpg      # App screenshot
└── src/
    ├── UI/
    │   └── base_layout.py     # Global styling / background
    ├── assets/                # Logos & static assets
    ├── components/
    │   ├── add_photos.py             # Upload attendance photos
    │   ├── attendance_result.py      # Attendance results dialog
    │   ├── auto_enroll_dialog.py     # Enroll via shared join link
    │   ├── create_subject.py         # Create-subject dialog
    │   ├── enroll_dialog.py          # Manual enroll-by-code dialog
    │   ├── footer.py
    │   ├── header.py
    │   ├── share_subject_code.py     # QR code / join link sharing
    │   ├── subject_card.py           # Subject card UI
    │   └── voice_attendance.py       # Voice attendance dialog
    ├── database/
    │   ├── config.py           # Supabase client setup
    │   └── db.py                # Database queries (teachers, students, subjects, logs)
    ├── pipeline/
    │   ├── face_pipeline.py    # Face embeddings, SVM training & prediction
    │   └── voice_pipeline.py   # Voice embeddings & speaker identification
    └── screens/
        ├── home_screen.py      # Landing screen (Teacher / Student)
        ├── teacher_screen.py   # Teacher dashboard
        └── student_screen.py   # Student dashboard & face-ID login
```

## Getting Started

### Prerequisites

- Python 3.9+
- A [Supabase](https://supabase.com/) project with `teachers`, `students`, `subjects`, `subject_student`, and `attendance_logs` tables
- `cmake` and build tools available on your system (required by `dlib`)

### Installation

```bash
git clone https://github.com/HimanshurajNimse/AttendAI.git
cd AttendAI
pip install -r requirements.txt
```

### Configuration

Create a `.streamlit/secrets.toml` file in the project root with your Supabase credentials:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-api-key"
```

### Run the app

```bash
streamlit run app.py
```

## Usage

1. **Teachers** register/log in, create subjects, and share the generated join link or QR code with students.
2. **Students** log in via their camera (face ID); first-time users register a profile with their face and, optionally, a short voice sample.
3. Students enroll in a subject by entering the subject code, scanning the QR code, or opening the shared join link.
4. To take attendance, teachers either:
   - upload classroom photo(s) and run **Face Analysis**, or
   - record classroom audio and run **Voice Attendance**.
5. Results are matched against enrolled students and logged automatically; teachers and students can review attendance history from their respective dashboards.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the repo and submit a pull request.

## License

No license has been specified for this repository yet. Please contact the repository owner before reuse or distribution.
