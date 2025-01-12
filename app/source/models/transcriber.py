# app/models/transcriber.py
import librosa
import whisper
import tempfile
import soundfile as sf
import requests
import numpy as np

from abc import ABC, abstractmethod


class AudioTranscriber(ABC):
    """Abstrakte Basisklasse für Audio-Transkription"""

    @abstractmethod
    def transcribe(self, audio_array, sample_rate):
        pass


class WhisperLocalTranscriber(AudioTranscriber):
    """Lokale Implementierung mit Whisper"""

    def __init__(self, model_name="tiny"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_array, sample_rate):
        if audio_array is None:
            return ""

        try:
            options = {
                "language": "de",
                "task": "transcribe",
                "beam_size": 3,  # Reduziert von default 5
                "best_of": 1,  # Reduziert von default 5
                "without_timestamps": True,
            }

            # Speichere Audio temporär
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
                sf.write(temp_audio.name, audio_array, sample_rate)
                result = self.model.transcribe(temp_audio.name, **options)
                return result["text"]

        except Exception as e:
            print(f"Transkriptionsfehler: {str(e)}")
            return ""


class VertexAITranscriber(AudioTranscriber):
    """Google Cloud Vertex AI Implementierung (Platzhalter)"""

    def __init__(self, project_id, location, model_id):
        # Hier später die Vertex AI Initialisierung
        pass

    def transcribe(self, audio_array, sample_rate):
        # Hier später die Vertex AI Implementation
        pass


class WhisperHuggingFaceTranscriber(AudioTranscriber):
    """Online Implementierung mit Whisper über Huggingface API"""

    def __init__(self, api_url, api_token):
        # Huggingface API URL für das Whisper-Modell
        self.api_url = api_url
        self.api_token = api_token

    def transcribe(self, audio_array, sample_rate):
        if audio_array is None:
            return ""

        try:
            # Ensure audio array is float32 and normalized between -1 and 1
            audio_array = audio_array.astype(np.float32)
            if np.abs(audio_array).max() > 1.0:
                audio_array = audio_array / np.abs(audio_array).max()

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
                # Use specific parameters for WAV file creation
                sf.write(
                    temp_audio.name,
                    audio_array,
                    sample_rate,
                    format='WAV',
                    subtype='FLOAT'  # Changed from PCM_16 to FLOAT
                )

                # Ensure file is written before sending
                temp_audio.flush()

                with open(temp_audio.name, "rb") as audio_file:
                    files = {"file": ("audio.wav", audio_file, "audio/wav")}  # Added content type
                    headers = {"Authorization": f"Bearer {self.api_token}"}
                    response = requests.post(self.api_url, files=files, headers=headers)

                    # Überprüfe die Antwort und extrahiere den Text
                    if response.status_code == 200:
                        result = response.json()
                        return result.get("text", "Fehler: Kein Transkriptions-Text in der Antwort.")
                    else:
                        # Extrahiere den Fehlertext aus der Antwort der API
                        error_message = response.json().get("error", "Unbekannter Fehler bei der Anfrage.")
                        return f"Fehler bei der Anfrage an Huggingface API: {response.status_code} - {error_message}"

        except Exception as e:
            answer = f"Transkriptionsfehler: {str(e)}"
            print(answer)
            return answer
