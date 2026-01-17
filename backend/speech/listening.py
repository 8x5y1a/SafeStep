import threading
import queue
import json
import os
import asyncio
import sounddevice as sd
from backend.speech.action import read_transcript
from vosk import Model, KaldiRecognizer
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("OPENROUTER_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "vosk-model-small-en-us-0.15")

model = Model(MODEL_PATH)
q = queue.Queue()

samplerate = 16000
KEYWORD = "jarvis"


def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))


def vosk_thread(loop, transcript_queue):
    recognizer = KaldiRecognizer(model, samplerate)

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

                if KEYWORD in text:
                    loop.call_soon_threadsafe(transcript_queue.put_nowait, text)


async def process_loop():
    while True:
        transcript = await transcript_queue.get()
        # background task
        asyncio.create_task(read_transcript(transcript))


async def main():
    global transcript_queue
    transcript_queue = asyncio.Queue()

    loop = asyncio.get_running_loop()
    thread = threading.Thread(
        target=vosk_thread, args=(loop, transcript_queue), daemon=True
    )
    thread.start()
    await process_loop()


if __name__ == "__main__":
    asyncio.run(main())
