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
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
                # Write the audio array to a temporary file
                sf.write(temp_audio.name, audio_array, sample_rate)
                temp_audio.flush()

                # Read and send the file directly as binary data
                with open(temp_audio.name, "rb") as audio_file:
                    headers = {"Authorization": f"Bearer {self.api_token}"}
                    response = requests.post(
                        self.api_url,
                        headers=headers,
                        data=audio_file
                    )

                    if response.status_code == 200:
                        return response.json().get("text", "")
                    else:
                        print(f"Response headers: {response.headers}")
                        print(f"Response content: {response.content}")
                        return f"Error: {response.status_code} - {response.json()}"

        except Exception as e:
            answer = f"Transcription error: {str(e)}"
            print(answer)
            return answer
