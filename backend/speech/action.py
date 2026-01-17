from textToSpeech import text_to_speech
from speechToText import transcription

def action (transcription):
        if "help" in transcription:
               help()
        if "What is around me" in transcription:
                see()

def help (transcription):
        text_to_speech("Please stay where you are. Someone is coming to help you.")


def see (transcription):
        #replace with vision code later