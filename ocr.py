"""
ocr.py
Text reading mode for VisionMate.

Captures a frame from the camera, runs on-device OCR (Tesseract) to
detect printed text such as signs, labels, or documents, and reads it
aloud. On Snapdragon hardware, this step can later be swapped for an
NPU-optimized OCR model from Qualcomm AI Hub for faster, lower-power
recognition; this prototype uses Tesseract as a CPU-based baseline.

Requires the Tesseract OCR engine installed on the system:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- After installing, set pytesseract.pytesseract.tesseract_cmd below
  to the install path if it isn't picked up automatically.
"""

import cv2
import pytesseract
from speak import say

# Uncomment and edit this line on Windows if Tesseract isn't found automatically:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run_text_reading():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Camera not found. Please check your webcam connection.")
        return

    say("Text reading mode started. Point the camera at text and press Space to read. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("VisionMate - Text Reading (Space=Read, Q=Quit)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray).strip()

            if text:
                say(f"I can read: {text}")
            else:
                say("No readable text found. Try moving closer or improving lighting.")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_text_reading()
