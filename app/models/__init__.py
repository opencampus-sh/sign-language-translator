# app/models/__init__.py
import os
from pathlib import Path
from huggingface_hub import login
from typing import Tuple, Union
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from .mock.model import MockWhisperForSignLanguage, MockWhisperProcessor

class ModelLoader:
    """Utility class for managing model loading and configuration"""
    
    DEFAULT_HF_MODEL = "your-org/sign-language-translator"  # Replace with your model
    
    @staticmethod
    def setup_huggingface_auth() -> None:
        """Setup Hugging Face authentication if needed"""
        if ModelLoader.is_using_mock():
            return
            
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        if hf_token:
            login(hf_token)

    @staticmethod
    def is_using_mock() -> bool:
        """Check if we should use mock model"""
        return os.getenv('USE_MOCK_MODEL', 'true').lower() == 'true'

    @staticmethod
    def get_model_path() -> str:
        """Get the appropriate model path based on environment"""
        if ModelLoader.is_using_mock():
            return str(Path(__file__).parent / 'mock')
        
        # For Hugging Face model
        return os.getenv('MODEL_PATH', ModelLoader.DEFAULT_HF_MODEL)

    @classmethod
    def load(cls) -> Tuple[Union[WhisperForConditionalGeneration, MockWhisperForSignLanguage], 
                          Union[WhisperProcessor, MockWhisperProcessor]]:
        """
        Load the appropriate model and processor
        
        Returns:
            Tuple containing:
            - Model (WhisperForConditionalGeneration or MockWhisperForSignLanguage)
            - Processor (WhisperProcessor or MockWhisperProcessor)
        """
        cls.setup_huggingface_auth()
        model_path = cls.get_model_path()
        
        if cls.is_using_mock():
            return (
                MockWhisperForSignLanguage.from_pretrained(model_path),
                MockWhisperProcessor()
            )
        
        # Load real model from Hugging Face
        auth_token = os.getenv('HUGGINGFACE_TOKEN')
        model = WhisperForConditionalGeneration.from_pretrained(
            model_path,
            use_auth_token=auth_token
        )
        processor = WhisperProcessor.from_pretrained(
            model_path,
            use_auth_token=auth_token
        )
        
        return model, processor

# Convenient function to load model and processor
def load_model_and_processor():
    """Convenience function to load model and processor"""
    return ModelLoader.load()

# Export the main interfaces
__all__ = ['ModelLoader', 'load_model_and_processor']