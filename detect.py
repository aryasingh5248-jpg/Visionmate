"""
detect.py
Object & obstacle detection mode for VisionMate.

Uses YOLOv8n (the smallest, fastest YOLOv8 variant) to detect objects
in the camera frame and announce what's ahead. On Snapdragon-powered
laptops, this same model can be exported through Qualcomm AI Hub and
run on the Hexagon NPU for much lower power draw and latency than
running it on CPU, which is what this prototype currently does.
"""

import cv2
import time
from ultralytics import YOLO
from speak import say

# YOLOv8n is downloaded automatically the first time this runs
model = YOLO("yolov8n.pt")

# Only announce objects we haven't just announced, to avoid spamming audio
COOLDOWN_SECONDS = 4
last_announced = {}


def describe_position(x_center, frame_width):
    """Roughly say whether an object is to the left, right, or ahead."""
    if x_center < frame_width / 3:
        return "on your left"
    elif x_center > 2 * frame_width / 3:
        return "on your right"
    else:
        return "ahead of you"


def run_object_detection():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Camera not found. Please check your webcam connection.")
        return

    say("Object detection started. Press Q on the video window to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)[0]
        frame_width = frame.shape[1]
        now = time.time()

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            if conf < 0.5:
                continue

            x1, y1, x2, y2 = box.xyxy[0]
            x_center = (x1 + x2) / 2
            position = describe_position(x_center, frame_width)

            # Draw box for the visual demo window
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Only speak if we haven't announced this object recently
            last_time = last_announced.get(label, 0)
            if now - last_time > COOLDOWN_SECONDS:
                say(f"{label} {position}")
                last_announced[label] = now

        cv2.imshow("VisionMate - Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_object_detection()
