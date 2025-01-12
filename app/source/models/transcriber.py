# app/models/transcriber.py
import librosa
import whisper
import tempfile
import soundfile as sf
import requests

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

        # Speichere Audio temporär (Whisper erwartet eine Datei)
        #with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
        #    sf.write(temp_audio.name, audio_array, sample_rate)

            # Transkribiere Audio
            #result = self.model.transcribe(temp_audio.name, language="de")
            #return result["text"]

        try:
            options = {
                "language": "de",
                "task": "transcribe",
                "beam_size": 3,     # Reduziert von default 5
                "best_of": 1,       # Reduziert von default 5
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
            # Konvertiere das Audio-Array zu Mono, falls es Stereo ist
            if len(audio_array.shape) > 1 and audio_array.shape[1] == 2:
                audio_array = np.mean(audio_array, axis=1)  # Stereo zu Mono

            # Temporäre Datei für das Audio erstellen
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
                # Speichern als WAV-Datei im richtigen Format (z.B. 16-bit PCM)
                sf.write(temp_audio.name, audio_array, sample_rate, subtype='PCM_16')  # 'PCM_16' für 16-bit WAV

                # Sende die Audiodatei an die Huggingface-API
                with open(temp_audio.name, "rb") as audio_file:
                    files = {"file": audio_file}
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

