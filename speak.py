"""
speak.py
Converts text to spoken audio on-device (no internet needed).
This is the shared voice output used by every VisionMate mode.
"""

import pyttsx3

# Initialize the TTS engine once and reuse it across the app
_engine = pyttsx3.init()
_engine.setProperty('rate', 165)   # words per minute, tuned for clarity
_engine.setProperty('volume', 1.0)


def say(text: str):
    """Speak the given text out loud and wait until it's done."""
    if not text:
        return
    print(f"[VisionMate says]: {text}")
    _engine.say(text)
    _engine.runAndWait()
