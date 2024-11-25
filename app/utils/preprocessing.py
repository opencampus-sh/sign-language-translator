# app/utils/preprocessing.py
import numpy as np
import torch
from typing import List, Dict, Union, Tuple
import logging

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
    logger = logging.getLogger(__name__)
    
    logger.debug(f"Input keypoints sequence length: {len(keypoints_sequence)}")
    processed_frames = []
    
    for i, frame_data in enumerate(keypoints_sequence):
        frame_features = []
        
        # Log frame data structure
        logger.debug(f"Frame {i} data keys: {frame_data.keys()}")
        logger.debug(f"Number of hands: {len(frame_data['hand_landmarks'])}")
        if frame_data['face_landmarks']:
            logger.debug(f"Number of face landmarks: {len(frame_data['face_landmarks'][0])}")
        
        # Process hands
        hand_landmarks = frame_data['hand_landmarks']
        for hand_idx in range(2):
            if hand_idx < len(hand_landmarks):
                points = hand_landmarks[hand_idx][:21]
                logger.debug(f"Hand {hand_idx} points shape: {len(points)}x{len(points[0])}")
                frame_features.extend([coord for point in points for coord in point])
            else:
                frame_features.extend([0.0] * (21 * 3))
        
        # Process face
        face_landmarks = frame_data['face_landmarks']
        if face_landmarks and len(face_landmarks) > 0:
            face_points = face_landmarks[0][:468]
            logger.debug(f"Face points shape: {len(face_points)}x{len(face_points[0])}")
            frame_features.extend([coord for point in face_points for coord in point])
        else:
            frame_features.extend([0.0] * (468 * 3))
        
        logger.debug(f"Frame {i} features length: {len(frame_features)}")
        processed_frames.append(frame_features)
    
    # Convert to tensor and log shapes
    tensor_data = torch.tensor(processed_frames, dtype=torch.float32)
    logger.debug(f"Tensor shape before normalization: {tensor_data.shape}")
    
    # Normalize and log final shape
    tensor_data = normalize_keypoints(tensor_data)
    logger.debug(f"Tensor shape after normalization: {tensor_data.shape}")
    
    return tensor_data.unsqueeze(0)

def normalize_keypoints(keypoints: torch.Tensor) -> torch.Tensor:
    """
    Normalize keypoint coordinates to be in range [-1, 1].
    
    Args:
        keypoints: Tensor of shape (sequence_length, feature_dimension)
    
    Returns:
        torch.Tensor: Normalized keypoints
    """
    # Reshape the keypoints to separate the coordinates
    # Original shape: (sequence_length, feature_dimension)
    # New shape: (sequence_length * n_points, 3)
    reshaped = keypoints.reshape(-1, 3)
    
    # Find min and max values for each coordinate across all frames
    # Skip zero-padded values in the calculation
    mask = reshaped != 0
    if not mask.any():
        return keypoints
    
    min_vals = reshaped[mask].min(dim=0)[0]
    max_vals = reshaped[mask].max(dim=0)[0]
    
    # Avoid division by zero
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1.0
    
    # Normalize non-zero values to [-1, 1]
    normalized = reshaped.clone()
    normalized[mask] = 2 * (reshaped[mask] - min_vals) / range_vals - 1
    
    # Reshape back to original dimensions
    return normalized.reshape(keypoints.shape)

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
