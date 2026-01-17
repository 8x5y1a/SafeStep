from client import get_client


def speech_to_text(audio_path: str) -> str:
    client = get_client()

    with open(audio_path, "rb") as audio_file:
        transcription = client.speech_to_text.convert(
            file=audio_file, model_id="scribe_v1"
        )

    print(transcription)

    # return transcription.
    return "test"
