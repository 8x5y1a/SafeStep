from elevenlabs import VoiceSettings
from client import get_client


def text_to_speech(
    text: str, output_path: str = "output.mp3", voice_id: str = "Rachel"
):
    client = get_client()

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.7),
    )

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Saved speech to {output_path}")
