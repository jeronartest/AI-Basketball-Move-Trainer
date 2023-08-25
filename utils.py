
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

enable_angles_view = False


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

    if "accuracy_rating" in context:
        height += 35
        accuracy_num = determine_accuracy_name(context['accuracy_rating'])
        cv2.putText(frame, "Accuracy Status: " + str(accuracy_num), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    if "r_area_arms" in context and enable_angles_view:
        height += 35
        r_area_arms_angle = determine_accuracy_name(context["r_area_arms"])
        cv2.putText(frame, "Right Area Arms Angle: " + str(r_area_arms_angle), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    if "r_area_side" in context and enable_angles_view:
        height += 35
        r_area_side = determine_accuracy_name(context["r_area_side"])
        cv2.putText(frame, "Right Area Sides Angle: " + str(r_area_side), (10, height),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    return frame


def determine_movement_type(argument: str, landmarks):
    if argument == 'basketball-move':
        return TypeOfMove(landmarks)
    return TypeOfExercise(landmarks)


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    if image is not None:
        (h, w) = image.shape[:2]
    else:
        (h, w) = (1920, 1080)

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    # return the resized image
    return resized
