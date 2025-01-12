# app/components/voicetospeech_model.py
import os
from dotenv import load_dotenv
from source.models.transcriber import WhisperHuggingFaceTranscriber, WhisperLocalTranscriber

# Globale Instanz des Transcribers
_transcriber = None
# Lädt die Variablen aus der .env-Datei
load_dotenv()


def get_transcriber():
    """Singleton-Pattern für den Transcriber"""
    global _transcriber
    if _transcriber is None:
        # Wähle hier die gewünschte Transcriber-Instanz
        use_huggingface = True  # Wechsel zwischen lokalem und Hugging Face Transcriber

        if use_huggingface:
            api_url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
            # api token from env-file
            api_token = os.getenv("HUGGINGFACE_TOKEN")
            _transcriber = WhisperHuggingFaceTranscriber(api_url, api_token)
        else:
            _transcriber = WhisperLocalTranscriber()

    return _transcriber


def transcribe(audio):
    """Transkribiert Audio-Input für das Gradio Interface"""
    if audio is None:
        return ""

    try:
        audio_array = audio[1]  # [0] ist sample_rate, [1] ist das Audio-Array
        sample_rate = audio[0]

        transcriber = get_transcriber()
        text = transcriber.transcribe(audio_array, sample_rate)
        return text
    except Exception as e:
        return f"Fehler bei der Transkription: {str(e)}"
