"""
face_recog.py
Known-face recognition mode for VisionMate.

Lets the user enroll a few known faces (family, friends) and then get
an audio alert when one of them appears in the camera view. Faces are
stored only as local numeric encodings on the user's own device -
never uploaded anywhere - which matters for both privacy and for
working fully offline.
"""

import cv2
import os
import pickle
import face_recognition
from speak import say

DATA_FILE = "known_faces.pkl"


def load_known_faces():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {"encodings": [], "names": []}


def save_known_faces(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)


def enroll_face():
    """Capture a photo and save it under a name the user provides."""
    name = input("Enter the name of the person to enroll: ").strip()
    if not name:
        print("No name entered, cancelling enrollment.")
        return

    cap = cv2.VideoCapture(0)
    say(f"Look at the camera. Press Space to capture a photo of {name}.")

    captured_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Enroll Face (Space=Capture, Q=Cancel)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            captured_frame = frame
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    rgb = cv2.cvtColor(captured_frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb)

    if not encodings:
        say("No face detected in that photo. Please try enrolling again.")
        return

    data = load_known_faces()
    data["encodings"].append(encodings[0])
    data["names"].append(name)
    save_known_faces(data)
    say(f"{name} has been enrolled successfully.")


def run_face_recognition():
    data = load_known_faces()
    if not data["encodings"]:
        say("No known faces enrolled yet. Please enroll a face first.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Camera not found. Please check your webcam connection.")
        return

    say("Face recognition started. Press Q to quit.")
    already_announced = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(data["encodings"], face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = data["names"][match_index]

                if name not in already_announced:
                    say(f"{name} is nearby")
                    already_announced.add(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("VisionMate - Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_face_recognition()
