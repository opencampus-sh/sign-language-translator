import torch
import time
from transformers import PretrainedConfig, WhisperForConditionalGeneration

class MockWhisperConfig(PretrainedConfig):
    model_type = "mock_whisper"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Required Whisper configuration attributes
        self.vocab_size = 51865
        self.num_mel_bins = 80
        self.d_model = 384
        self.encoder_attention_heads = 6
        self.encoder_layers = 4
        self.encoder_ffn_dim = 1536
        self.decoder_attention_heads = 6
        self.decoder_layers = 4
        self.decoder_ffn_dim = 1536
        self.max_source_positions = 1500
        self.max_target_positions = 448
        self.dropout = 0.0
        self.attention_dropout = 0.0
        self.activation_dropout = 0.0
        self.encoder_layerdrop = 0.0
        self.decoder_layerdrop = 0.0
        self.pad_token_id = 50256
        self.bos_token_id = 50256
        self.eos_token_id = 50256
        self.suppress_tokens = None
        self.begin_suppress_tokens = [220, 50256]
        self.decoder_start_token_id = 50257
        self.use_cache = True
        self.is_encoder_decoder = True
        self.activation_function = "gelu"
        self.init_std = 0.02
        self.scale_embedding = False
        self.use_weighted_layer_sum = False
        self.classifier_proj_size = 256
        self.apply_spec_augment = False
        self.mask_time_prob = 0.05
        self.mask_time_length = 10
        self.mask_time_min_masks = 2
        self.mask_feature_prob = 0.0
        self.mask_feature_length = 10
        self.mask_feature_min_masks = 0
        self.median_filter_width = 7

class MockWhisperForSignLanguage(WhisperForConditionalGeneration):
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
        config = MockWhisperConfig()
        model = cls(config)
        return model

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
