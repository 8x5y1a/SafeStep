from elevenlabs import VoiceSettings
from backend.speech.client import get_client
import sounddevice as sd
import numpy as np


def text_to_speech(text: str, voice_id: str = "goT3UYdM9bhm0n2lmKQx"):
    client = get_client()

    audio = client.text_to_speech.stream(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="pcm_22050",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.7),
    )

    # stream(audio)
    with sd.OutputStream(
        samplerate=22050,
        channels=1,
        dtype="int16",
    ) as stream:
        for chunk in audio:
            if isinstance(chunk, bytes):
                pcm = np.frombuffer(chunk, dtype=np.int16)
                stream.write(pcm.reshape(-1, 1))
