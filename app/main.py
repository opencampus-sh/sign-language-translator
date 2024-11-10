# app/main.py
from flask import Flask, request, jsonify
import cv2
import os
from models import load_model_and_processor, ModelLoader
from utils.keypoint_extraction import KeypointExtractor
from utils.preprocessing import preprocess_keypoints
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Initialize components
keypoint_extractor = KeypointExtractor()
model, processor = load_model_and_processor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_type': 'mock' if ModelLoader.is_using_mock() else 'production',
        'model_path': ModelLoader.get_model_path()
    })

@app.route('/process-sign-language', methods=['POST'])
def process_sign_language():
    """Process video and translate sign language."""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        temp_path = '/tmp/temp_video.mp4'
        video_file.save(temp_path)
        
        try:
            # Process video frames
            cap = cv2.VideoCapture(temp_path)
            keypoints_sequence = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                keypoints = keypoint_extractor.extract_keypoints(frame)
                keypoints_sequence.append(keypoints)
            
            cap.release()
        finally:
            # Ensure temporary file is removed
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        if not keypoints_sequence:
            return jsonify({'error': 'No frames could be extracted from video'}), 400
        
        # Preprocess and get prediction
        model_input = preprocess_keypoints(keypoints_sequence)
        outputs = model.generate(model_input)
        transcription = processor.decode(outputs[0])
        
        return jsonify({
            'transcription': transcription,
            'model_type': 'mock' if ModelLoader.is_using_mock() else 'production',
            'frames_processed': len(keypoints_sequence),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
