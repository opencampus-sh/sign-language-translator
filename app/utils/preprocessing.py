# app/utils/preprocessing.py
import numpy as np
import torch
from typing import List, Dict, Union, Tuple

def preprocess_keypoints(keypoints_sequence: List[Dict]) -> torch.Tensor:
    """
    Preprocess a sequence of keypoints for model input.
    
    Args:
        keypoints_sequence: List of dictionaries containing 'hand_landmarks' and 'face_landmarks'
            Each landmark is a list of points with x, y, z coordinates
    
    Returns:
        torch.Tensor: Preprocessed keypoints in the format expected by the model
        Shape: (1, sequence_length, feature_dimension)
    """
    processed_frames = []
    
    for frame_data in keypoints_sequence:
        frame_features = []
        
        # Process hand landmarks
        hand_landmarks = frame_data['hand_landmarks']
        # Handle up to 2 hands
        for i in range(2):
            if i < len(hand_landmarks):
                # Each hand has 21 landmarks with 3 coordinates (x, y, z)
                hand_points = hand_landmarks[i]
                frame_features.extend([coord for point in hand_points for coord in point])
            else:
                # Pad with zeros if hand is missing
                frame_features.extend([0.0] * (21 * 3))
        
        # Process face landmarks
        face_landmarks = frame_data['face_landmarks']
        if face_landmarks:
            # Take the first face if multiple are detected
            face_points = face_landmarks[0]
            # MediaPipe face mesh has 468 landmarks with 3 coordinates each
            frame_features.extend([coord for point in face_points for coord in point])
        else:
            # Pad with zeros if no face is detected
            frame_features.extend([0.0] * (468 * 3))
        
        processed_frames.append(frame_features)
    
    # Convert to tensor and add batch dimension
    # Shape: (1, sequence_length, n_features)
    tensor_data = torch.tensor(processed_frames, dtype=torch.float32)
    
    # Normalize the coordinates
    tensor_data = normalize_keypoints(tensor_data)
    
    return tensor_data.unsqueeze(0)

def normalize_keypoints(keypoints: torch.Tensor) -> torch.Tensor:
    """
    Normalize keypoint coordinates to be in range [-1, 1].
    
    Args:
        keypoints: Tensor of shape (sequence_length, feature_dimension)
    
    Returns:
        torch.Tensor: Normalized keypoints
    """
    # Find min and max values for each coordinate across all frames
    # Skip zero-padded values in the calculation
    mask = keypoints != 0
    if not mask.any():
        return keypoints
    
    min_vals = keypoints[mask].reshape(-1, 3).min(dim=0)[0]
    max_vals = keypoints[mask].reshape(-1, 3).max(dim=0)[0]
    
    # Avoid division by zero
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1.0
    
    # Normalize non-zero values to [-1, 1]
    normalized = keypoints.clone()
    normalized[mask] = 2 * (keypoints[mask] - min_vals.reshape(-1, 3)) / range_vals.reshape(-1, 3) - 1
    
    return normalized

def get_feature_dimension() -> int:
    """
    Calculate the feature dimension for the model input.
    
    Returns:
        int: Total number of features per frame
    """
    n_hand_landmarks = 21  # MediaPipe hands has 21 landmarks per hand
    n_hands = 2  # We process up to 2 hands
    n_face_landmarks = 468  # MediaPipe face mesh has 468 landmarks
    n_coordinates = 3  # Each landmark has x, y, z coordinates
    
    total_features = (n_hand_landmarks * n_hands + n_face_landmarks) * n_coordinates
    return total_features

# Optional: Add augmentation functions for training
def augment_keypoints(
    keypoints: torch.Tensor,
    rotation_range: float = 0.1,
    scale_range: float = 0.1,
    translation_range: float = 0.1
) -> torch.Tensor:
    """
    Apply random augmentations to keypoint sequences.
    Only used during training.
    
    Args:
        keypoints: Tensor of shape (batch_size, sequence_length, feature_dimension)
        rotation_range: Maximum rotation in radians
        scale_range: Maximum scale factor variation
        translation_range: Maximum translation factor
    
    Returns:
        torch.Tensor: Augmented keypoints
    """
    # This is a placeholder for actual augmentation logic
    # Implement based on your specific needs during training
    return keypoints
