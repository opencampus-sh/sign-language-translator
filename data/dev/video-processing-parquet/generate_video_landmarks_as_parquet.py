import pandas as pd
import requests
import mediapipe as mp
import cv2
import os
import json
from natsort import natsorted

# Function to download a file from a URL
def download_file(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name}. Status code: {response.status_code}")

# Define expected number of landmarks for each type
EXPECTED_LANDMARKS = {
    'pose': 33,
    'face': 468,
    'left_hand': 21,
    'right_hand': 21
}

# Define batch size for processing
BATCH_SIZE = 1000  # Adjust this based on your available memory

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
    """
    Create column selectors for facial and pose landmarks from the given indices.
    """
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
    """
    Filter the DataFrame to include only the specified landmarks.
    """
    columns = create_landmark_column_filters(facial_landmarks, pose_landmarks)
    return df[columns]

def process_batch(start_frame, end_frame, cap, holistic, video_file_name):
    """
    Process a batch of frames and return the landmark data.
    """
    frame_data = {}
    frame_count = start_frame - 1
    
    while frame_count < end_frame and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Initialize frame data dictionary with zeros
        current_frame_data = {'frame': frame_count}
        
        for landmark_type, num_landmarks in EXPECTED_LANDMARKS.items():
            for idx in range(num_landmarks):
                current_frame_data[f'{landmark_type}-{idx}-x'] = 0
                current_frame_data[f'{landmark_type}-{idx}-y'] = 0
                current_frame_data[f'{landmark_type}-{idx}-z'] = 0
                current_frame_data[f'{landmark_type}-{idx}-visibility'] = 0
        
        # Get frame dimensions and crop
        height, width, _ = frame.shape
        right_half = frame[:, width // 2:]
        image = cv2.cvtColor(right_half, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = holistic.process(image)
        
        # Save visualization every 1000 frames
        if frame_count % 1000 == 0:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, results.pose_landmarks, mp.solutions.holistic.POSE_CONNECTIONS)
            if results.face_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, results.face_landmarks, mp.solutions.face_mesh.FACEMESH_TESSELATION)
            if results.left_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
            if results.right_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    image, results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS)
            
            output_path = os.path.join('output_frames', f'frame_{frame_count}.jpg')
            cv2.imwrite(output_path, image)
        
        # Update landmarks when detected
        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                current_frame_data[f'pose-{idx}-x'] = landmark.x
                current_frame_data[f'pose-{idx}-y'] = landmark.y
                current_frame_data[f'pose-{idx}-z'] = landmark.z
                current_frame_data[f'pose-{idx}-visibility'] = landmark.visibility
        
        if results.face_landmarks:
            for idx, landmark in enumerate(results.face_landmarks.landmark):
                current_frame_data[f'face-{idx}-x'] = landmark.x
                current_frame_data[f'face-{idx}-y'] = landmark.y
                current_frame_data[f'face-{idx}-z'] = landmark.z
                current_frame_data[f'face-{idx}-visibility'] = 1
        
        if results.left_hand_landmarks:
            for idx, landmark in enumerate(results.left_hand_landmarks.landmark):
                current_frame_data[f'left_hand-{idx}-x'] = landmark.x
                current_frame_data[f'left_hand-{idx}-y'] = landmark.y
                current_frame_data[f'left_hand-{idx}-z'] = landmark.z
                current_frame_data[f'left_hand-{idx}-visibility'] = 1
        
        if results.right_hand_landmarks:
            for idx, landmark in enumerate(results.right_hand_landmarks.landmark):
                current_frame_data[f'right_hand-{idx}-x'] = landmark.x
                current_frame_data[f'right_hand-{idx}-y'] = landmark.y
                current_frame_data[f'right_hand-{idx}-z'] = landmark.z
                current_frame_data[f'right_hand-{idx}-visibility'] = 1
        
        frame_data[frame_count] = current_frame_data
        
        if frame_count % 100 == 0:
            print(f"Processing frame {frame_count}")
    
    return frame_data

def save_batch_to_parquet(frame_data, output_file, mode='w'):
    """
    Save batch data to a parquet file.
    """
    # Convert frame data to DataFrame
    df = pd.DataFrame.from_dict(frame_data, orient='index')
    
    # Sort columns
    cols = ['frame'] + sorted([col for col in df.columns if col != 'frame'])
    df = df[cols]
    
    # Save to parquet
    if mode == 'w':
        df.to_parquet(output_file, index=False, engine="pyarrow")
    else:
        # Append to existing file
        existing_df = pd.read_parquet(output_file)
        combined_df = pd.concat([existing_df, df])
        combined_df.to_parquet(output_file, index=False, engine="pyarrow")

def main():
    # Read CSV and get video URL
    csv_file_path = 'tagesschau_sign_language_video_links.csv'
    tagesschau_links_df = pd.read_csv(csv_file_path)
    video_url = tagesschau_links_df['webm'].iloc[-1]
    
    # Download video
    video_file_name = video_url.split('/')[-1]
    download_file(video_url, video_file_name)
    
    # Initialize Mediapipe
    mp_holistic = mp.solutions.holistic
    
    # Create output directories
    os.makedirs('output_frames', exist_ok=True)
    os.makedirs('output_json', exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(video_file_name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {total_frames}")
    
    # Process video in batches
    with mp_holistic.Holistic(static_image_mode=False,
                             model_complexity=2,
                             enable_segmentation=True,
                             refine_face_landmarks=True) as holistic:
        
        for batch_start in range(0, total_frames, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, total_frames)
            print(f"Processing batch: frames {batch_start} to {batch_end}")
            
            # Process batch
            frame_data = process_batch(batch_start, batch_end, cap, holistic, video_file_name)
            
            # Save batch
            mode = 'w' if batch_start == 0 else 'a'
            save_batch_to_parquet(frame_data, f"{video_file_name}.parquet", mode)
            
            # Save JSON checkpoint
            with open(f"output_json/{video_file_name}_batch_{batch_start}.json", "w") as f:
                json.dump(frame_data, f)
            
            # Clear frame data to free memory
            del frame_data
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Apply final filtering
    print("Applying final landmark filtering...")
    final_df = pd.read_parquet(f"{video_file_name}.parquet")
    filtered_df = filter_landmarks_df(final_df, all_facial_landmarks, pose_landmarks)
    filtered_df = filtered_df[natsorted(filtered_df.columns)]
    filtered_df.to_parquet(f"{video_file_name}_filtered.parquet", engine="pyarrow")
    print("Processing complete!")

if __name__ == "__main__":
    main()