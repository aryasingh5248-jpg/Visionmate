"""
main.py
VisionMate - Offline AI Visual Assistant
Entry point: a simple voice-guided menu that launches each mode.

Run this file to start the app:
    python main.py
"""

from speak import say
from detect import run_object_detection
from ocr import run_text_reading
from face_recog import run_face_recognition, enroll_face


def show_menu():
    print("\n===== VisionMate =====")
    print("1. Object & Obstacle Detection")
    print("2. Read Text Aloud (OCR)")
    print("3. Recognize Known Faces")
    print("4. Enroll a New Face")
    print("5. Exit")
    return input("Choose an option (1-5): ").strip()


def main():
    say("Welcome to Vision Mate. Your offline visual assistant.")

    while True:
        choice = show_menu()

        if choice == "1":
            run_object_detection()
        elif choice == "2":
            run_text_reading()
        elif choice == "3":
            run_face_recognition()
        elif choice == "4":
            enroll_face()
        elif choice == "5":
            say("Goodbye.")
            break
        else:
            say("Invalid option. Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
