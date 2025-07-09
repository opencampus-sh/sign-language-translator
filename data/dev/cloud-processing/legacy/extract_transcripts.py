def extract_transcripts(input_path: str, temp_dir: str) -> str:
    """Extract audio transcript from video using Whisper.
    
    Args:
        input_path: Path to the input video file
        temp_dir: Directory for temporary files and output
        
    Returns:
        str: Path to the output JSON file containing transcripts with timestamps
    """
    import whisper
    import json
    import os
    import subprocess
    
    # Extract audio from video
    audio_path = os.path.join(temp_dir, "audio.wav")
    command = [
        'ffmpeg',
        '-i', input_path,
        '-ar', '16000',  # Sample rate required by Whisper
        '-ac', '1',      # Mono audio
        audio_path
    ]
    subprocess.run(command, check=True)
    
    try:
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
        output_path = os.path.join(
            temp_dir, 
            f"{os.path.splitext(os.path.basename(input_path))[0]}_transcript.json"
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(word_segments, f, ensure_ascii=False, indent=2)
        
        return output_path
        
    finally:
        # Clean up temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path) 