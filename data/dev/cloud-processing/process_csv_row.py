def process_csv_row(input_path: str, temp_dir: str) -> str:
    """
    Process a single CSV row file - download video from URL and extract landmarks and transcripts.
    
    This function is designed to work with CloudProcessor.submit_job().
    
    Args:
        input_path: Path to the JSON file containing CSV row data
        temp_dir: Directory for temporary files and output
        
    Returns:
        str: Path to the output directory containing processed files
    """
    import json
    import os
    import requests
    import cv2
    import pandas as pd
    import mediapipe as mp
    import whisper
    import subprocess
    from natsort import natsorted
    
    # Read CSV row data from JSON file
    with open(input_path, "r", encoding="utf-8") as f:
        row_data = json.load(f)
    
    video_url = row_data.get("webm")  # Use medium quality
    video_id = row_data.get("date", "unknown") + "_" + row_data.get("time", "unknown").replace(":", "")
    
    if not video_url:
        raise ValueError("No video URL found in row data")
    
    print(f"Processing video: {video_id}")
    print(f"Video URL: {video_url}")
    
    # Download video
    video_filename = f"{video_id}.mp4"
    video_path = os.path.join(temp_dir, video_filename)
    
    print(f"Downloading video...")
    response = requests.get(video_url, stream=True, timeout=300)
    if response.status_code == 200:
        with open(video_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                if chunk:
                    f.write(chunk)
        print(f"Downloaded video: {video_filename}")
    else:
        raise Exception(f"Failed to download video. Status code: {response.status_code}")
    
    # Define expected number of landmarks
    EXPECTED_LANDMARKS = {
        "pose": 33,
        "face": 468,
        "left_hand": 21,
        "right_hand": 21
    }
    
    # Extract landmarks
    print("Extracting landmarks...")
    mp_holistic = mp.solutions.holistic
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {total_frames}")
    
    frame_data = {}
    
    # Process video for landmarks
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
            current_frame_data = {"frame": frame_count}
            
            for landmark_type, num_landmarks in EXPECTED_LANDMARKS.items():
                for idx in range(num_landmarks):
                    current_frame_data[f"{landmark_type}-{idx}-x"] = 0
                    current_frame_data[f"{landmark_type}-{idx}-y"] = 0
                    current_frame_data[f"{landmark_type}-{idx}-z"] = 0
                    current_frame_data[f"{landmark_type}-{idx}-visibility"] = 0
            
            # Get frame dimensions and crop to right half (where sign language interpreter is)
            height, width, _ = frame.shape
            right_half = frame[:, width // 2:]
            image = cv2.cvtColor(right_half, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = holistic.process(image)
            
            # Update landmarks when detected
            if results.pose_landmarks:
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    current_frame_data[f"pose-{idx}-x"] = landmark.x
                    current_frame_data[f"pose-{idx}-y"] = landmark.y
                    current_frame_data[f"pose-{idx}-z"] = landmark.z
                    current_frame_data[f"pose-{idx}-visibility"] = landmark.visibility
            
            if results.face_landmarks:
                for idx, landmark in enumerate(results.face_landmarks.landmark):
                    current_frame_data[f"face-{idx}-x"] = landmark.x
                    current_frame_data[f"face-{idx}-y"] = landmark.y
                    current_frame_data[f"face-{idx}-z"] = landmark.z
                    current_frame_data[f"face-{idx}-visibility"] = 1
            
            if results.left_hand_landmarks:
                for idx, landmark in enumerate(results.left_hand_landmarks.landmark):
                    current_frame_data[f"left_hand-{idx}-x"] = landmark.x
                    current_frame_data[f"left_hand-{idx}-y"] = landmark.y
                    current_frame_data[f"left_hand-{idx}-z"] = landmark.z
                    current_frame_data[f"left_hand-{idx}-visibility"] = 1
            
            if results.right_hand_landmarks:
                for idx, landmark in enumerate(results.right_hand_landmarks.landmark):
                    current_frame_data[f"right_hand-{idx}-x"] = landmark.x
                    current_frame_data[f"right_hand-{idx}-y"] = landmark.y
                    current_frame_data[f"right_hand-{idx}-z"] = landmark.z
                    current_frame_data[f"right_hand-{idx}-visibility"] = 1
            
            frame_data[frame_count] = current_frame_data
            
            if frame_count % 500 == 0:
                print(f"Processing frame {frame_count}")
                
            frame_count += 1
    
    cap.release()
    
    # Save landmarks to parquet
    landmarks_output = os.path.join(temp_dir, f"{video_id}_landmarks.parquet")
    df = pd.DataFrame.from_dict(frame_data, orient="index")
    df = df[["frame"] + natsorted([col for col in df.columns if col != "frame"])]
    df.to_parquet(landmarks_output, engine="pyarrow")
    print(f"Saved landmarks: {landmarks_output}")
    
    # Extract transcripts
    print("Extracting transcripts...")
    
    # Extract audio from video
    audio_path = os.path.join(temp_dir, f"{video_id}_audio.wav")
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ar", "16000",  # Sample rate required by Whisper
        "-ac", "1",      # Mono audio
        "-y",            # Overwrite output file
        audio_path
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True)
        print("Audio extracted successfully")
        
        # Load Whisper model
        model = whisper.load_model("large-v3")
        
        # Transcribe audio with word-level timestamps
        result = model.transcribe(
            audio_path,
            language="de",  # German language
            word_timestamps=True  # Enable word-level timestamps
        )
        
        # Extract word segments
        word_segments = result.get("segments", [])
        
        # Save transcription to JSON
        transcript_output = os.path.join(temp_dir, f"{video_id}_transcript.json")
        
        with open(transcript_output, "w", encoding="utf-8") as f:
            json.dump(word_segments, f, ensure_ascii=False, indent=2)
        
        print(f"Saved transcript: {transcript_output}")
        
    except subprocess.CalledProcessError as e:
        print(f"Warning: Audio extraction failed: {e}")
        # Create empty transcript file
        transcript_output = os.path.join(temp_dir, f"{video_id}_transcript.json")
        with open(transcript_output, "w", encoding="utf-8") as f:
            json.dump([], f)
    
    finally:
        # Clean up temporary files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)
    
    print(f"Processing complete for {video_id}")
    return landmarks_output  # Return the landmarks file path 

if __name__ == "__main__":    
    input_path = "/home/jku/sign-language-translator/test_data/csv_folder/row_000000.json"
    temp_dir = "/home/jku/sign-language-translator/test_data/temp_dir"
    output_path = process_csv_row(input_path, temp_dir)
    print(f"Output saved to: {output_path}")