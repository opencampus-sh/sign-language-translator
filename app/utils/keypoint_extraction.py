import mediapipe as mp
import cv2
import numpy as np

class KeypointExtractor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7
        )
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.7
        )

    def extract_keypoints(self, frame):
        """Extract hand and face keypoints from a frame."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process hands
        hand_results = self.hands.process(frame_rgb)
        hand_landmarks = []
        if hand_results.multi_hand_landmarks:
            for landmarks in hand_results.multi_hand_landmarks:
                hand_points = []
                for point in landmarks.landmark:
                    hand_points.append([point.x, point.y, point.z])
                hand_landmarks.append(hand_points)
        
        # Process face
        face_results = self.face_mesh.process(frame_rgb)
        face_landmarks = []
        if face_results.multi_face_landmarks:
            for landmarks in face_results.multi_face_landmarks:
                face_points = []
                for point in landmarks.landmark:
                    face_points.append([point.x, point.y, point.z])
                face_landmarks.append(face_points)
        
        return {
            'hand_landmarks': hand_landmarks,
            'face_landmarks': face_landmarks
        }
