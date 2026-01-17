from textToSpeech import text_to_speech
from speechToText import transcription

def action (transcription):
  # Ask ai what is actually asked: 
    # 1 : Asking to see around?
        # Do nothing, send code to abal
    # 2 : Asking for help?
        # Ask ai based on transcription, what would be a good response saying something like this specifically to the scenario: Please stay where you are. Someone is coming to help you.
    # 3 : Nothing important
      #  Return: "None"!

        if "help" in transcription:
               help()
        if "What is around me" in transcription:
                see()

def help ():
        text_to_speech("Please stay where you are. Someone is coming to help you.")


def see ():
  
        #replace with vision code later