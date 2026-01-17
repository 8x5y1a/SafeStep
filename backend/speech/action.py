from backend.speech.textToSpeech import text_to_speech
from backend.services.gemini import prompt_gemini
from dotenv import load_dotenv
import os
import requests
from backend.vision.vision import observe_camera

load_dotenv()

prompt_context = "You will be given a transcript, from this transcript you must correctly select one of the following options:  1. Is the user asking to see what is around him (Usage of word like 'show me' or 'what is nearby', etc.) 2. Is the user asking for help (Words like 'I need help' or 'I need assistance', etc.) 3. Nothing above. You must return the appropriate prompt based on the selection. If 3: Answer: 'Nothing', If 2: Take the context of the transcript to say something that essentially says something like this: 'Someone is coming to help you' or 'Someone will come to assist you shortly', but make sure to personalize it. If 1: return 'Vision'. Do not add anything else to the answer of the prompt. The following text is the transcript: "
isVisionRequested = False


async def read_transcript(transcription: str):
    print("Transcript: " + transcription)

    # Figure out what the user is requesting
    answer = await prompt_gemini(prompt_context + transcription)
    if answer == "Nothing":
        print("nothing to do")
        return
    if answer == "Vision":
        print("VISION ")
        answer = await observe_camera()
        if answer:
            text_to_speech(answer)
        else:
            print("NO ANSWER PROVIDED")
        return

    requests.post(str(os.getenv("NGROK_URL")) + "/broadcast")  # json={"info": "TODO:"}
    print(answer)
    text_to_speech(answer)
