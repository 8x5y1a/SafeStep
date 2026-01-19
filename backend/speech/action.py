from backend.speech.textToSpeech import text_to_speech
from backend.services.gemini import prompt_gemini
from dotenv import load_dotenv
import os
import requests
from backend.vision.vision import observe_camera
import pygame
import time
import threading

load_dotenv()

prompt_context = "You will be given a transcript, from this transcript you must correctly select one of the following options:  1. Is the user asking to see what is around him (Usage of word like 'show me' or 'what is nearby', etc.) 2. Is the user asking for help (Words like 'I need help' or 'I need assistance', etc.) 3. Nothing above. You must return the appropriate prompt based on the selection. If 3: Answer: 'Nothing', If 2: Take the context of the transcript to say something that essentially says something like this: 'A volunteer is coming to help you' or 'A volunteer will come to assist you shortly', but make sure to personalize it. If 1: return 'Vision'. Do not add anything else to the answer of the prompt. The following text is the transcript: "
isVisionRequested = False


async def read_transcript(transcription: str):
    pygame.mixer.init()
    pygame.mixer.music.load("soundEffect.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    print("Transcript: " + transcription)

    # Figure out what the user is requesting
    answer = await prompt_gemini(prompt_context + transcription)
    print(answer)
    if answer == "Nothing":
        print("nothing to do")
        return
    if answer == "Vision":
        answer = await observe_camera()
        if answer:
            print(" .")
            text_to_speech(answer, str(os.getenv("VOICE_ID")))
        else:
            print("NO ANSWER PROVIDED")
        return

    t = threading.Thread(
        target=text_to_speech, args=(answer, str(os.getenv("VOICE_ID")))
    )

    t.start()
    try:
        requests.post(
            str(os.getenv("NGROK_URL")) + "/broadcast", timeout=8
        )  # json={"info": "TODO:"}
    except:
        print("error with website")
