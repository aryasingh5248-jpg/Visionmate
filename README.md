# VisionMate — Offline AI Visual Assistant

VisionMate is an offline, privacy-first desktop app built for the **Snapdragon AI Lab Build & Present Challenge**. It's designed to help visually impaired users understand their surroundings using real-time computer vision, running entirely on-device on Snapdragon-powered HP laptops — no internet connection or cloud processing required.

## What it does

VisionMate has three modes, each triggered from a simple voice-guided menu:

1. **Object & Obstacle Detection** — uses the laptop camera to detect nearby objects (people, furniture, doors, etc.) and announces what's around and roughly which direction it's in.
2. **Text Reading (OCR)** — reads printed text out loud from signs, labels, or documents held up to the camera.
3. **Known Face Recognition** — lets a user enroll a few familiar people (family, friends) and get notified by name when one of them is nearby.

All feedback is delivered through speech, so the app can be used without looking at the screen at all.

## Why this matters for Snapdragon

The current prototype runs its models on CPU using standard open-source libraries (YOLOv8n, Tesseract OCR, face_recognition) so it can be demoed quickly during the challenge window. The next step — and the core reason this fits the Snapdragon AI Lab challenge — is porting these models through **Qualcomm AI Hub** to run on the Hexagon NPU instead of the CPU. That would mean:

- Much lower latency, since running three CV tasks live requires fast per-frame inference
- Much lower power draw, which matters because this is meant to be used for long stretches during someone's day
- The ability to run all three detection modes simultaneously without the laptop fan spinning up

This project is intentionally structured with each capability in its own module (`detect.py`, `ocr.py`, `face_recog.py`) so each one can be swapped for a Qualcomm AI Hub–optimized version independently.

## Project structure

```
VisionMate/
├── main.py          # Entry point with the voice-guided menu
├── detect.py         # Object & obstacle detection (YOLOv8n)
├── ocr.py             # Text reading (Tesseract OCR)
├── face_recog.py     # Face enrollment & recognition
├── speak.py           # Shared text-to-speech helper
├── requirements.txt   # Python dependencies
└── README.md
```

## Setup

1. **Install Python 3.10+** if you don't have it already.
2. **Install Tesseract OCR** (required for text reading):
   - Windows: [UB-Mannheim Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - After installing, if `ocr.py` can't find it automatically, uncomment the path line at the top of `ocr.py` and point it to your install location.
3. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```
   python main.py
   ```

## Usage

- Choose an option from the menu (1–5) using your keyboard.
- In camera windows, press **Q** to quit that mode and return to the menu.
- In text reading mode, press **Space** to capture and read text, **Q** to quit.
- Enroll a face first (option 4) before trying face recognition (option 3).

## Roadmap

- [ ] Port YOLOv8n, OCR, and face embedding models through Qualcomm AI Hub for NPU acceleration
- [ ] Add distance estimation (not just direction) for obstacle detection
- [ ] Package as a standalone installer for non-technical users
- [ ] Add multi-language support for text reading and voice output

## Team / Author

Built by Arya Singh for the Snapdragon AI Lab Build & Present Challenge (Qualcomm).
