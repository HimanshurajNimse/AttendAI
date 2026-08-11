import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return sp, facerec


def get_face_embeddings(image_np):
    import cv2

    sp, facerec = load_dlib_models()

    rgb = image_np.copy()

    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces_cv = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )
    st.write("Faces Found:", len(faces_cv))

    for (x, y, w, h) in faces_cv:
        st.write(f"x={x}, y={y}, w={w}, h={h}")
    encodings = []

    for (x, y, w, h) in faces_cv:

        rect = dlib.rectangle(
            int(x),
            int(y),
            int(x + w),
            int(y + h)
        )

        shape = sp(rgb, rect)

        descriptor = facerec.compute_face_descriptor(
            rgb,
            shape
        )

        encodings.append(np.array(descriptor))
    st.write("Embeddings:", len(encodings))

    return encodings


def get_trained_model():
    X = []
    y = []

    students = get_all_students()

    if not students:
        return None

    for student in students:
        embedding = student.get("face_embedding")

        if embedding is not None:
            X.append(np.array(embedding))
            y.append(student["student_id"])

    if len(X) == 0:
        return None

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    if len(set(y)) < 2:
        return {
            "clf": None,
            "X": X,
            "y": y
        }

    clf.fit(X, y)

    return {
        "clf": clf,
        "X": X,
        "y": y
    }

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)

def predict_attendance(image_np):
    encodings = get_face_embeddings(image_np)

    detected_students = {}

    model = get_trained_model()

    if model is None:
        return detected_students, [], len(encodings)

    clf = model["clf"]
    X_train = model["X"]
    y_train = model["y"]

    all_students = sorted(set(y_train))

    for encoding in encodings:

        if clf is not None:
            predicted_id = clf.predict([encoding])[0]
        else:
            # Only one student in the database
            predicted_id = all_students[0]

        idx = y_train.index(predicted_id)
        student_embedding = X_train[idx]

        distance = np.linalg.norm(student_embedding - encoding)

        if distance <= 0.6:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)