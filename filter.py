import cv2
import numpy as np
import requests
import util

def  crop_thumbnail(image_url) -> bool:
    resp = requests.get(image_url, stream=True)
    img = cv2.imdecode(
        np.asarray(bytearray(resp.content), dtype=np.uint8),
        cv2.IMREAD_COLOR
    )
    cropped_img = util.crop_image_region(img, util.PRESET_REGIONS["bottom"])
    
    return cropped_img

def has_ui_colors(cropped_img, threshold=10):
    hsv_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    
    blue_lower = np.array([100, 80, 80])
    blue_upper = np.array([140, 255, 255])

    red_lower1 = np.array([0, 80, 80])
    red_upper1 = np.array([10, 255, 255])

    red_lower2 = np.array([160, 80, 80])
    red_upper2 = np.array([180, 255, 255])
    
    
    blue_mask = cv2.inRange(hsv_img, blue_lower, blue_upper)
    red_mask1 = cv2.inRange(hsv_img, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv_img, red_lower2, red_upper2)
    
    score = blue_mask.mean() + red_mask1.mean() + red_mask2.mean()
    
    return score > threshold

    
def filter_gameplay_clips(clip_data):
    gameplay_clips = []
    for clip in clip_data:
        cropped_thumbnail = crop_thumbnail(clip["thumbnail_url"])
        # e se thumbnail_url nao estiver disponivel? vale a pena tirar screenshot do video? 
        if has_ui_colors(cropped_thumbnail):
            gameplay_clips.append(clip)
    return gameplay_clips