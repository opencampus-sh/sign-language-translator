# Mock Whisper Model Configuration

This configuration file (`config.json`) defines the architecture and parameters for our mock sign language translation model.

## Model Architecture

- **Model Type**: Whisper-based architecture adapted for sign language
- **Is Mock**: True (indicates this is a mock/test implementation)
- **Feature Size**: 1554
  - Calculated from:
    - 2 hands × 21 landmarks × 3 coordinates (126)
    - 468 face landmarks × 3 coordinates (1404)
    - Total: 1554 features

## Model Parameters

- **Hidden Layers**: 2
- **Hidden Size**: 128
- **Intermediate Size**: 512
- **Attention Heads**: 4
- **Vocabulary Size**: 5 (number of predefined responses)
- **Max Position Embeddings**: 512

## Predefined Responses

The model outputs one of these predefined responses:

- 0: "Hello! Nice to meet you."
- 1: "Thank you very much!"
- 2: "Goodbye, see you later!"
- 3: "How are you?"
- 4: "My name is John."

## Token IDs

- **Pad Token**: 0
- **BOS Token**: 1 (Beginning of Sequence)
- **EOS Token**: 2 (End of Sequence)

## Model Info

- **Name/Path**: mock_whisper
- **Transformers Version**: 4.30.0
