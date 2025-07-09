import pandas as pd
import os
from natsort import natsorted

# Landmark definitions
# Silhouette/face contour
silhouette = [
    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
    397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
]

# Lips landmarks
lips_upper_outer = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
lips_lower_outer = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
lips_upper_inner = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
lips_lower_inner = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

# Right eye landmarks
right_eye_upper0 = [246, 161, 160, 159, 158, 157, 173]
right_eye_lower0 = [33, 7, 163, 144, 145, 153, 154, 155, 133]
right_eye_upper1 = [247, 30, 29, 27, 28, 56, 190]
right_eye_lower1 = [130, 25, 110, 24, 23, 22, 26, 112, 243]
right_eye_upper2 = [113, 225, 224, 223, 222, 221, 189]
right_eye_lower2 = [226, 31, 228, 229, 230, 231, 232, 233, 244]
right_eye_lower3 = [143, 111, 117, 118, 119, 120, 121, 128, 245]
right_eyebrow_upper = [156, 70, 63, 105, 66, 107, 55, 193]
right_eyebrow_lower = [35, 124, 46, 53, 52, 65]
right_eye_iris = [473, 474, 475, 476, 477]

# Left eye landmarks
left_eye_upper0 = [466, 388, 387, 386, 385, 384, 398]
left_eye_lower0 = [263, 249, 390, 373, 374, 380, 381, 382, 362]
left_eye_upper1 = [467, 260, 259, 257, 258, 286, 414]
left_eye_lower1 = [359, 255, 339, 254, 253, 252, 256, 341, 463]
left_eye_upper2 = [342, 445, 444, 443, 442, 441, 413]
left_eye_lower2 = [446, 261, 448, 449, 450, 451, 452, 453, 464]
left_eye_lower3 = [372, 340, 346, 347, 348, 349, 350, 357, 465]
left_eyebrow_upper = [383, 300, 293, 334, 296, 336, 285, 417]
left_eyebrow_lower = [265, 353, 276, 283, 282, 295]
left_eye_iris = [468, 469, 470, 471, 472]

# Nose landmarks
nose_landmarks = {
    'midway_between_eyes': [168],
    'nose_tip': [1],
    'nose_bottom': [2],
    'nose_right_corner': [98],
    'nose_left_corner': [327]
}

# Cheek landmarks
cheek_landmarks = {
    'right_cheek': [205],
    'left_cheek': [425]
}

# Combine all landmarks
right_eye_all = (right_eye_upper0 + right_eye_lower0 + right_eye_upper1 +
                 right_eye_lower1 + right_eye_upper2 + right_eye_lower2 +
                 right_eye_lower3 + right_eye_iris)
left_eye_all = (left_eye_upper0 + left_eye_lower0 + left_eye_upper1 +
                left_eye_lower1 + left_eye_upper2 + left_eye_lower2 +
                left_eye_lower3 + left_eye_iris)
right_eyebrow_all = right_eyebrow_upper + right_eyebrow_lower
left_eyebrow_all = left_eyebrow_upper + left_eyebrow_lower
lips_all = (lips_upper_outer + lips_lower_outer +
           lips_upper_inner + lips_lower_inner)
nose_all = (nose_landmarks['nose_tip'] +
           nose_landmarks['nose_bottom'])

# Create final combined list of all facial landmarks
all_facial_landmarks = (
    silhouette +
    lips_all +
    right_eye_all +
    left_eye_all +
    right_eyebrow_all +
    left_eyebrow_all +
    nose_all +
    cheek_landmarks['right_cheek'] +
    cheek_landmarks['left_cheek']
)

# Remove duplicates while maintaining order
all_facial_landmarks = list(dict.fromkeys(all_facial_landmarks))
pose_landmarks = [11, 12, 13, 14, 15, 16, 23, 24]

def create_landmark_column_filters(facial_landmarks, pose_landmarks):
    """Create column selectors for facial and pose landmarks from the given indices."""
    columns_to_select = []
    
    for landmark in facial_landmarks:
        columns_to_select.extend([
            f'face-{landmark}-visibility',
            f'face-{landmark}-x',
            f'face-{landmark}-y',
            f'face-{landmark}-z'
        ])
    
    for landmark in pose_landmarks:
        columns_to_select.extend([
            f'pose-{landmark}-visibility',
            f'pose-{landmark}-x',
            f'pose-{landmark}-y',
            f'pose-{landmark}-z'
        ])
    
    return columns_to_select

def filter_landmarks_df(df, facial_landmarks, pose_landmarks):
    """Filter the DataFrame to include only the specified landmarks."""
    columns = create_landmark_column_filters(facial_landmarks, pose_landmarks)
    return df[columns]

def filter_landmarks(input_path: str, temp_dir: str) -> str:
    """Filter a single landmark file to extract relevant features."""
    # Read the full landmarks
    df = pd.read_parquet(input_path)
    
    # Filter landmarks
    filtered_df = filter_landmarks_df(df, all_facial_landmarks, pose_landmarks)
    filtered_df = filtered_df[natsorted(filtered_df.columns)]
    
    # Save filtered landmarks
    output_path = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_filtered.parquet")
    filtered_df.to_parquet(output_path, engine="pyarrow")
    
    return output_path 