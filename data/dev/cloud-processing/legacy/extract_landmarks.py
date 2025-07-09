def extract_landmarks(input_path: str, temp_dir: str) -> str:
    """Process a single video file and return the path to the output file with all landmarks."""
    import mediapipe as mp
    import cv2
    import pandas as pd
    import os
    from natsort import natsorted
    
    # Initialize MediaPipe
    mp_holistic = mp.solutions.holistic
    
    # Define expected number of landmarks
    EXPECTED_LANDMARKS = {
        'pose': 33,
        'face': 468,
        'left_hand': 21,
        'right_hand': 21
    }
    
    # Open video
    cap = cv2.VideoCapture(input_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_data = {}
    
    # Process video
    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=True,
        refine_face_landmarks=True
    ) as holistic:
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
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
                
            frame_count += 1
    
    cap.release()
    
    # Save to parquet
    output_path = os.path.join(temp_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}.parquet")
    df = pd.DataFrame.from_dict(frame_data, orient='index')
    df = df[['frame'] + sorted([col for col in df.columns if col != 'frame'])]
    df.to_parquet(output_path, engine="pyarrow")
    
    return output_path 