import numpy as np
from body_part_angle import BodyPartAngle
from utils import *


class TypeOfMove(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    def kobe_fade(self, accuracy, status):

        nose = detection_body_part(self.landmarks, "NOSE")
        left_elbow = detection_body_part(self.landmarks, "LEFT_ELBOW")
        right_elbow = detection_body_part(self.landmarks, "RIGHT_ELBOW")
        avg_shoulder_y = (left_elbow[1] + right_elbow[1])

        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_left_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle)

        left_leg_angle = self.angle_of_the_right_leg()
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) 

        while nose[1] < avg_shoulder_y:
            arm_angle_result = avg_arm_angle
        else:
            if nose[1] < avg_shoulder_y:
                status = True

        # TODO: Return a counter & a status
        return [0, status]

    def calculate_exercise(self, move_type, accuracy, status):
        if move_type == "kobe-fade":
            return self.kobe_fade(
                accuracy, status)    

        # TODO: Return a counter & a status
        return [0, status]
