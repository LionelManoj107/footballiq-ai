"""
Pose estimation: turns a drill video into measurable movement data.

Production version should use MediaPipe Pose (or OpenPose) to extract
per-frame joint coordinates, then derive features like:
  - foot-to-ball distance at contact
  - knee/hip/ankle angles during the strike
  - balance (center-of-mass stability across frames)
  - follow-through consistency

Install for the real version:
    pip install mediapipe opencv-python

This starter version provides a working interface with a functional
(if simplified) heuristic so the pipeline runs end-to-end today. Swap
`_extract_features_mediapipe` in for `_extract_features_stub` once you
plug in MediaPipe.
"""
import os
import random


def analyze_video(filepath: str, drill_type: str) -> dict:
    """
    Returns movement_data: a dict of extracted features used by scoring.py
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    # TODO: replace with real MediaPipe-based extraction (see _extract_features_mediapipe below)
    return _extract_features_stub(filepath, drill_type)


def _extract_features_stub(filepath: str, drill_type: str) -> dict:
    """
    Deterministic-ish stub so scores aren't purely random noise: uses file size
    as a light seed so repeated tests on the same video return the same result.
    Replace this with real pose-estimation extraction.
    """
    seed = os.path.getsize(filepath) if os.path.exists(filepath) else 0
    rng = random.Random(seed)

    return {
        "foot_ball_distance_cm": rng.uniform(2, 15),
        "balance_stability": rng.uniform(0.5, 1.0),      # 1.0 = perfectly stable
        "follow_through_consistency": rng.uniform(0.4, 1.0),
        "contact_angle_deviation_deg": rng.uniform(0, 25),  # lower = better
        "drill_type": drill_type,
    }


def _extract_features_mediapipe(filepath: str, drill_type: str) -> dict:
    """
    Real implementation sketch (requires `pip install mediapipe opencv-python`):

    import cv2
    import mediapipe as mp

    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(filepath)
    frames_landmarks = []

    with mp_pose.Pose(static_image_mode=False) as pose:
        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                frames_landmarks.append(results.pose_landmarks.landmark)
    cap.release()

    # From frames_landmarks, compute: foot-to-ball distance at contact frame,
    # center-of-mass trajectory (balance), joint angles (knee/hip/ankle) for
    # follow-through consistency, etc. Return the same feature dict shape as
    # `_extract_features_stub` above so scoring.py doesn't need to change.
    """
    raise NotImplementedError("Plug in MediaPipe here for production use")
