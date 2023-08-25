import cv2
import argparse
from utils import *
import mediapipe as mp
from body_part_angle import BodyPartAngle
from types_of_exercise import TypeOfExercise


ap = argparse.ArgumentParser()
# Adds an optional argument
ap.add_argument("-mt",
                "--move-type",
                type=str,
                help="The types of move type",
                required=False)
# Adds the argument (-t for exercise type) and adds the argument to the argument parser
ap.add_argument("-t",
                "--action-type",
                type=str,
                help='Type of activity to do',
                required=True)
ap.add_argument("-vs",
                "--video_source",
                type=str,
                help='Type of activity to do',
                required=False)
args = vars(ap.parse_args())
args = vars(ap.parse_args())
args = vars(ap.parse_args())

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


if args["video_source"] is not None:
    cap = cv2.VideoCapture(args["video_source"])
else:
    cap = cv2.VideoCapture(0)  # webcam

cap.set(3, 800)  # width
cap.set(4, 480)  # height

# setup mediapipe
with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    ctx = {}  # movement of exercise
    action_type = args["action_type"]
    move_type = args["move_type"]
    while cap.isOpened():
        ret, frame = cap.read()
        # result_screen = np.zeros((250, 400, 3), np.uint8)
        frame = cv2.resize(frame, (720, 1280), interpolation=cv2.INTER_AREA)
        # recolor frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # make detection
        results = pose.process(frame)
        # recolor back to BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            move_type_inst = determine_movement_type(move_type, landmarks)
            ctx = move_type_inst.calculate_exercise(
                action_type, ctx)
        except:
            pass

        frame = score_table(move_type, action_type, frame, ctx)

        # render detections (for landmarks)
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255),
                                   thickness=2,
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(174, 139, 45),
                                   thickness=2,
                                   circle_radius=2),
        )

        cv2.imshow('Video', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()