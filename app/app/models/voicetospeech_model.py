# app/components/voicetospeech_model.py
from app.models.transcriber import WhisperLocalTranscriber

# Globale Instanz des Transcribers
_transcriber = None


def get_transcriber():
    """Singleton-Patterns für den Transcriber"""
    global _transcriber
    if _transcriber is None:
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
