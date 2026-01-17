import sounddevice as sd
import queue
import json
import os
import time
from vosk import Model, KaldiRecognizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "vosk-model-small-en-us-0.15")

model = Model(MODEL_PATH)

q = queue.Queue()


def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))


samplerate = 16000

# Create recognizer for keyword spotting
recognizer = KaldiRecognizer(model, samplerate)

# Hardcode keyword
KEYWORD = "hello"


def listen_forever():
    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    ):
        print("Listening...")

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                # Check for keyword
                if KEYWORD in text:
                    print("Keyword detected! Transcribing...")

                    # Now start transcription mode
                    transcribe_mode()


def transcribe_mode():
    # Create new recognizer for transcription
    rec = KaldiRecognizer(model, samplerate)
    rec = KaldiRecognizer(model, samplerate)

    print("Recording... (speak now)")

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("Transcription:", result.get("text", ""))
            # TODO: Send to the Olivier's code to determine what we need
            break


if __name__ == "__main__":
    listen_forever()
