import cv2
import mediapipe as mp
import pandas as pd


class PoseDetector:
    #############################################
    # Carefull! Mediapipe uses all the time all landmarks, even if a subset is requested
    # This setting is only for saving the landmarks after media pipe has processed them

    LANDMARK_CONFIGS = {
        'face': {
            'none': [],
            'minimal': [10, 152, 234, 454],  # Four points
            'basic': list(range(0, 468, 10)),  # Every 10th point
            'full': list(range(468))  # All points
        },
        'hand': {
            'none': [],
            'minimal': [0, 4, 8, 12, 16, 20],
            'basic': [0, 2, 4, 5, 8, 9, 12, 13, 16, 17, 20],
            'full': list(range(21))
        },
        'pose': {
            'none': [],
            'minimal': [0, 11, 12, 13, 14, 15, 16],
            'basic': list(range(0, 25, 2)),
            'full': list(range(25))
        }
    }

    def __init__(self, track_config=None):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Initialize tracking configuration
        self.track_config = track_config if track_config else {
            key: value['basic'] for key, value in self.LANDMARK_CONFIGS.items()
        }

        # Initialize Holistic model
        self.holistic = mp.solutions.holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            enable_segmentation=False,
            smooth_landmarks=True,
            model_complexity=2
        )

    def _draw_landmarks(self, frame, results):
        """Draws landmarks on the frame."""
        if results.face_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.face_landmarks, self.mp_holistic.FACEMESH_CONTOURS)
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)
        if results.left_hand_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        if results.right_hand_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS)
        return frame

    def _extract_landmarks(self, results):
        """Extracts landmarks from the results."""
        landmarks = {}

        # Extract landmarks based on the tracking configuration
        if results.face_landmarks and self.track_config.get('face') != "none":
            for idx in self.LANDMARK_CONFIGS['face'].get(self.track_config.get('face', 'none'), []):
                landmark = results.face_landmarks.landmark[idx]
                landmarks[f'face_{idx}'] = [landmark.x, landmark.y, landmark.z]

        if results.left_hand_landmarks and self.track_config.get('leftHand') != "none":
            for idx in self.LANDMARK_CONFIGS['hand'].get(self.track_config.get('leftHand', 'none'), []):
                landmark = results.left_hand_landmarks.landmark[idx]
                landmarks[f'left_hand_{idx}'] = [landmark.x, landmark.y, landmark.z]

        if results.right_hand_landmarks and self.track_config.get('rightHand') != "none":
            for idx in self.LANDMARK_CONFIGS['hand'].get(self.track_config.get('rightHand', 'none'), []):
                landmark = results.right_hand_landmarks.landmark[idx]
                landmarks[f'right_hand_{idx}'] = [landmark.x, landmark.y, landmark.z]

        if results.pose_landmarks and self.track_config.get('pose') != "none":
            for idx in self.LANDMARK_CONFIGS['pose'].get(self.track_config.get('pose', 'none'), []):
                landmark = results.pose_landmarks.landmark[idx]
                landmarks[f'pose_{idx}'] = [landmark.x, landmark.y, landmark.z]

        return landmarks

    def process_live(self, frame):
        """Process a single frame for live processing."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(frame_rgb)

        # Extract landmarks and draw them on the frame
        landmarks = self._extract_landmarks(results)
        annotated_frame = self._draw_landmarks(frame.copy(), results)

        return annotated_frame, landmarks

    @staticmethod
    def create_landmark_dataframe(landmarks):
        """Converts landmarks into a pandas DataFrame."""
        return pd.DataFrame([{
            'frame': data['frame'],
            'timestamp': data['timestamp'],
            **{f"{k}_x": v[0] for k, v in data['landmarks'].items()},
            **{f"{k}_y": v[1] for k, v in data['landmarks'].items()},
            **{f"{k}_z": v[2] for k, v in data['landmarks'].items()}
        } for data in landmarks])
