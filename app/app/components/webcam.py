import time
import gradio as gr
import numpy as np
import pandas as pd
import tempfile
from threading import Lock
from config.settings import WEBCAM_SETTINGS
from app.components.mediapipe_model import PoseDetector

# Global variables initialized with default values
processed_csv_path = None
detector = None
recording_frames = []
recording = True
last_config = None
recording_lock = Lock()

webcam_input = None
processed_video = None

# Config
face_detail_live = "minimal"
hand_detail_live = "basic"
pose_detail_live = "none"


def initialize_detector(face_detail, hand_detail, pose_detail):
    """Initializes the PoseDetector with the provided configuration."""
    new_config = {
        'face': face_detail if face_detail != "none" else None,
        'leftHand': hand_detail if hand_detail != "none" else None,
        'rightHand': hand_detail if hand_detail != "none" else None,
        'pose': pose_detail if pose_detail != "none" else None
    }

    # Only initialize the detector if the configuration has changed
    global detector, last_config
    if detector is None or last_config != new_config:
        print(f"Initializing detector with config: {new_config}")
        detector = PoseDetector(track_config=new_config)
        last_config = new_config.copy()


def process_live_frame(frame):
    """Processes a single frame for live video input."""
    global recording_frames, recording_lock

    # Sicherstellen, dass ein Bild vorhanden ist
    if frame is None:
        reset_detector()
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Schwarzes Bild
        return dummy_frame, "No input frame detected"

    # Initialize detector if configuration changes
    initialize_detector(face_detail_live, hand_detail_live, pose_detail_live)

    # Process frame and extract landmarks
    try:
        annotated_frame, landmarks = detector.process_live(frame)
        if not isinstance(annotated_frame, np.ndarray):
            print("annotated_frame is not a valid image")
            annotated_frame = None
    except Exception as e:
        print(f"Error during frame processing: {repr(e)}")
        return frame, "Error during processing", "⚪ Error"

    # Display active recognition details
    preview_text = (
        f"Active Recognition: "
        f"Face: {face_detail_live} | "
        f"Hands: {hand_detail_live} | "
        f"Pose: {pose_detail_live} \n \n"
    )

    # Handle recording if active
    if recording and landmarks:
        record_frame_data(landmarks)

    # Show recent recorded data
    preview_text += f"\n\nRecorded Frames: {len(recording_frames)}\n\n"
    preview_text += f"Last Data Points:\n{get_recent_recorded_data()}"

    # Secure output frame
    output_frame = annotated_frame if annotated_frame is not None else frame

    # Convert recording_frames to list of lists
    recording_frames_list = [[frame['frame'], frame['timestamp'], str(frame['landmarks'])] for frame in recording_frames]

    return output_frame, preview_text, get_recording_status(), recording_frames_list


def reset_detector():
    """Resets the detector and configuration."""
    global detector, last_config
    detector = None
    last_config = None


def record_frame_data(landmarks):
    """Stores the frame data for recording."""
    frame_data = {
        'frame': len(recording_frames),
        'timestamp': time.time(),
        'landmarks': landmarks
    }

    # Safely update the recording frames list
    with recording_lock:
        recording_frames.append(frame_data)


def get_recent_recorded_data():
    """Returns the most recent recorded frame data as a string."""
    with recording_lock:
        df = detector.create_landmark_dataframe(recording_frames[-10:])
    return df.tail().to_string()


def get_recording_status():
    """Returns the current recording status as a string."""
    return '🔴 Recording in progress' if recording_frames else '⚪ Waiting for recording...'


def update_csv(recording_frames):
    df = pd.DataFrame(recording_frames, columns=["frame", "timestamp", "landmarks"])
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', prefix='recording_frames_') as temp_file:
        df.to_csv(temp_file, index=False)
        return temp_file.name


def create_webcam_component():
    global webcam_input, processed_video

    """Creates and returns the webcam component with the UI."""
    with gr.Column(variant="panel") as webcam_component:
        webcam_input = gr.Image(
            height=WEBCAM_SETTINGS['height'],
            label=WEBCAM_SETTINGS['label'],
            sources=["webcam"],
            streaming=True,
            mirror_webcam=True,
            visible=True
        )

        processed_video = gr.Image(
            height=WEBCAM_SETTINGS['height'],
            label=WEBCAM_SETTINGS['label'],
            streaming=True,
            visible=True
        )

        status_text = gr.Textbox(label="Recording Status", interactive=False)

    with gr.Accordion("Debug Area", open=False) as debug_area:

        # with gr.Row():
        #     csv_output_live = gr.File(
        #         label="Recorded Keypoint Data (CSV)",
        #         interactive=False,
        #         file_types=[".csv"]
        #     )
        #with gr.Row():
        recording_frames_csv = gr.File(
            label="Download CSV",
            file_count="single",
            visible=True,
            interactive=False,
        )
        recording_frames_output = gr.DataFrame(
            label="Recorded Keypoint Data",
            headers=["frame", "timestamp", "landmarks"],
            datatype=["number", "number", "str"],
            col_count=(3, "fixed"),
            wrap=True,
            row_count=10,
        )
        with gr.Row():
            csv_preview = gr.Textbox(
                label="Live Data Preview",
                interactive=False,
                lines=10,
                max_lines=10,
                autoscroll=True
            )

    # Event Handler
    webcam_input.stream(
        fn=process_live_frame,
        inputs=[webcam_input],
        outputs=[processed_video, csv_preview, status_text, recording_frames_output]
    )

    recording_frames_output.change(
        update_csv,
        inputs=[recording_frames_output],
        outputs=[recording_frames_csv]
    )

    return webcam_component, debug_area
