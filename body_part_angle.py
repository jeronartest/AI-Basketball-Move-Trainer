import mediapipe as mp
import pandas as pd
import numpy as np
import cv2


class BodyPartAngle:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def calculate_position(self, body_part):
        from utils import detection_body_part
        return detection_body_part(self.landmarks, body_part)

    def angle_of_the_right_area_arms(self):
        from utils import detection_body_part
        r_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        from utils import calculate_angle
        return calculate_angle(r_elbow, r_shoulder, l_shoulder)

    def angle_of_the_right_area_side(self):
        from utils import detection_body_part
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        r_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        from utils import calculate_angle
        return calculate_angle(r_shoulder, r_hip, r_knee)

    def angle_of_the_left_arm(self):
        from utils import detection_body_part
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        l_wrist = detection_body_part(self.landmarks, "LEFT_WRIST")
        from utils import calculate_angle
        return calculate_angle(l_shoulder, l_elbow, l_wrist)
    
    def angle_of_the_right_arm(self):
        from utils import detection_body_part
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection_body_part(self.landmarks, "RIGHT_WRIST")
        from utils import calculate_angle
        return calculate_angle(r_shoulder, r_elbow, r_wrist)

    def angle_of_the_left_leg(self):
        from utils import detection_body_part
        l_hip = detection_body_part(self.landmarks, "LEFT_HIP")
        l_knee = detection_body_part(self.landmarks, "LEFT_KNEE")
        l_ankle = detection_body_part(self.landmarks, "LEFT_ANKLE")
        from utils import calculate_angle
        return calculate_angle(l_hip, l_knee, l_ankle)

    def angle_of_the_right_leg(self):
        from utils import detection_body_part
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        r_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection_body_part(self.landmarks, "RIGHT_ANKLE")
        from utils import calculate_angle
        return calculate_angle(r_hip, r_knee, r_ankle)

    def angle_of_the_neck(self):
        from utils import detection_body_part, calculate_angle
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        r_mouth = detection_body_part(self.landmarks, "MOUTH_RIGHT")
        l_mouth = detection_body_part(self.landmarks, "MOUTH_LEFT")
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        l_hip = detection_body_part(self.landmarks, "LEFT_HIP")

        shoulder_avg = [(r_shoulder[0] + l_shoulder[0]) / 2,
                        (r_shoulder[1] + l_shoulder[1]) / 2]
        mouth_avg = [(r_mouth[0] + l_mouth[0]) / 2,
                     (r_mouth[1] + l_mouth[1]) / 2]
        hip_avg = [(r_hip[0] + l_hip[0]) / 2, (r_hip[1] + l_hip[1]) / 2]

        return abs(180 - calculate_angle(mouth_avg, shoulder_avg, hip_avg))

    def angle_of_the_abdomen(self):
        from utils import detection_body_part, calculate_angle
        # calculate angle of the avg shoulder
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        shoulder_avg = [(r_shoulder[0] + l_shoulder[0]) / 2,
                        (r_shoulder[1] + l_shoulder[1]) / 2]

        # calculate angle of the avg hip
        r_hip = detection_body_part(self.landmarks, "RIGHT_HIP")
        l_hip = detection_body_part(self.landmarks, "LEFT_HIP")
        hip_avg = [(r_hip[0] + l_hip[0]) / 2, (r_hip[1] + l_hip[1]) / 2]

        # calculate angle of the avg knee
        r_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        l_knee = detection_body_part(self.landmarks, "LEFT_KNEE")
        knee_avg = [(r_knee[0] + l_knee[0]) / 2, (r_knee[1] + l_knee[1]) / 2]

        return calculate_angle(shoulder_avg, hip_avg, knee_avg)
