
import mediapipe as mp
import pandas as pd
import numpy as np
import cv2

from types_of_exercise import TypeOfExercise
from types_of_moves import TypeOfMove

mp_pose = mp.solutions.pose

accuracy_him = 0
accuracy_goat = 1
accuracy_legend = 2
accuracy_allstar = 3
accuracy_league = 4


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def detection_body_part(landmarks, body_part_name):
    val = mp_pose.PoseLandmark[body_part_name].value
    if not landmarks[val]:
        return [0, 0, False]
    return [
        landmarks[val].x,
        landmarks[val].y,
        landmarks[val].visibility
    ]


def detection_body_parts(landmarks):
    body_parts = pd.DataFrame(columns=["body_part", "x", "y"])

    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection_body_part(landmarks, lndmrk)
        body_parts.loc[i] = lndmrk, cord[0], cord[1]

    return body_parts


def determine_accuracy_name(index):
    if index == accuracy_allstar:
        return "Allstar"
    if index == accuracy_legend:
        return "Legend"
    if index == accuracy_league:
        return "League"
    if index == accuracy_goat:
        return "Goat"
    if index == accuracy_him:
        return "Him"
    # Just get good
    return "Bum"


def score_table(move_type, action_type, frame, context):
    height = 65
    cv2.putText(frame, "Move Type : " + move_type.replace("-", " "),
                (10, height), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
                cv2.LINE_AA)
    height += 35
    cv2.putText(frame, "Exercise Type : " + action_type.replace("-", " "),
                (10, height), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
                cv2.LINE_AA)

    if "counter" in context:
        height += 35
        counter = context['counter']
        cv2.putText(frame, "Counter : " + str(counter), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    if "status" in context:
        height += 35
        status = context['status']
        cv2.putText(frame, "Status : " + str(status), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    if "accuracy" in context:
        height += 35
        status = context['accuracy']
        cv2.putText(frame, "Accuracy : " + str(status), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    if "accuracy_num" in context:
        height += 35
        accuracy_num = determine_accuracy_name(context['accuracy_num'])
        cv2.putText(frame, "Accuracy Status: " + str(accuracy_num), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    return frame


def determine_movement_type(argument: str, landmarks):
    if argument == 'basketball-move':
        return TypeOfMove(landmarks)
    return TypeOfExercise(landmarks)
