# app/models/transcriber.py
import whisper
import tempfile
import soundfile as sf
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
