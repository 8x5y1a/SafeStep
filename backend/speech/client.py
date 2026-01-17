import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()


def get_client() -> ElevenLabs:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    return ElevenLabs(api_key=api_key)
