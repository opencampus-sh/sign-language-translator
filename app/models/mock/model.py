import torch
import time
from transformers import PreTrainedModel, WhisperPreTrainedModel

class MockWhisperForSignLanguage(WhisperPreTrainedModel):
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
        config = type('Config', (), {'n_positions': 512})()
        return cls(config)

    def __init__(self, config):
        super().__init__(config)
        self.common_signs = {
            0: "Hello! Nice to meet you.",
            1: "Thank you very much!",
            2: "Goodbye, see you later!",
            3: "How are you?",
            4: "My name is John.",
        }

    def generate(self, input_features, **kwargs):
        time.sleep(0.5)
        batch_size = input_features.shape[0]
        sequence_length = input_features.shape[1]
        output_idx = sequence_length % len(self.common_signs)
        return torch.tensor([[output_idx]])

class MockWhisperProcessor:
    def decode(self, token_ids, **kwargs):
        common_signs = {
            0: "Hello! Nice to meet you.",
            1: "Thank you very much!",
            2: "Goodbye, see you later!",
            3: "How are you?",
            4: "My name is John.",
        }
        return common_signs[token_ids[0].item()]
