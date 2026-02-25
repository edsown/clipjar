import cv2
import numpy as np
import requests
from config import MOTION_THRESHOLD
import util
import os
import logging

logger = logging.getLogger(__name__)

def has_motion(video_path, motion_threshold=MOTION_THRESHOLD, sample_frames=30):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        logger.error(f"Could not open video: {video_path}")
        return False
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = max(1, total_frames // sample_frames)
    
    prev_frame = None
    motion_scores = []
    
    for i in range(0, total_frames, frame_step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if prev_frame is not None:
            frame_diff = cv2.absdiff(prev_frame, gray)
            motion_score = np.mean(frame_diff)
            motion_scores.append(motion_score)
        
        prev_frame = gray
    
    cap.release()
    
    if not motion_scores:
        return False
    
    avg_motion = np.mean(motion_scores)
    logger.debug(f"Average motion score for {os.path.basename(video_path)}: {avg_motion:.2f}")
    
    return avg_motion > motion_threshold


def filter_clips_with_motion(clip_paths, motion_threshold=MOTION_THRESHOLD):
    active_clips = []
    for path in clip_paths:
        if has_motion(path, motion_threshold=motion_threshold):
            active_clips.append(path)
        else:
            logger.info(f"Filtered out static clip: {os.path.basename(path)}")
    
    return active_clips