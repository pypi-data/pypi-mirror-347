# facetracker/tracker.py
import os
import cv2
import face_recognition
import pickle
import sys
import threading
import time

recognized_people = set()
_previous_line_length = 0
_recognition_started = False
_reference_dir = None
_encoding_cache = None


def _load_reference_encodings():
    global _encoding_cache
    if os.path.exists(_encoding_cache):
        with open(_encoding_cache, "rb") as f:
            return pickle.load(f)

    encodings = {}
    for person in os.listdir(_reference_dir):
        person_folder = os.path.join(_reference_dir, person)
        if not os.path.isdir(person_folder):
            continue

        for img_file in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_file)
            try:
                image = face_recognition.load_image_file(img_path)
                face_encs = face_recognition.face_encodings(image)
                if face_encs:
                    encodings.setdefault(person, []).append(face_encs[0])
            except Exception:
                continue

    if encodings:
        with open(_encoding_cache, "wb") as f:
            pickle.dump(encodings, f)
    return encodings


def _recognize_face(face_encoding, known_encodings):
    for name, enc_list in known_encodings.items():
        matches = face_recognition.compare_faces(enc_list, face_encoding)
        if any(matches):
            return name
    return "Unknown"


def _background_loop():
    global recognized_people, _previous_line_length
    known_encodings = _load_reference_encodings()
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FPS, 30)

    while True:
        ret, frame = capture.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        current_faces = set()
        for face_encoding in face_encodings:
            name = _recognize_face(face_encoding, known_encodings)
            current_faces.add(name)

        if current_faces != recognized_people:
            recognized_people = current_faces
            output_text = f"People in frame: {', '.join(sorted(recognized_people))}"
            padding = ' ' * max(0, _previous_line_length - len(output_text))
            sys.stdout.write('\r' + output_text + padding)
            sys.stdout.flush()
            _previous_line_length = len(output_text)

        time.sleep(0.1)


def start_recognition(faces_dir="Faces"):
    global _reference_dir, _encoding_cache, _recognition_started
    if _recognition_started:
        return

    _reference_dir = os.path.abspath(faces_dir)
    _encoding_cache = os.path.join(_reference_dir, "face_encodings.pkl")

    if not os.path.isdir(_reference_dir):
        raise FileNotFoundError(f"Faces directory not found: {_reference_dir}")

    thread = threading.Thread(target=_background_loop, daemon=True)
    thread.start()
    _recognition_started = True
