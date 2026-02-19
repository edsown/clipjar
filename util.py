import os


PRESET_REGIONS = {
    "top": {"x_start_ratio": 0, "x_end_ratio": 1, "y_start_ratio": 0, "y_end_ratio": 0.2},
    "bottom": {"x_start_ratio": 0, "x_end_ratio": 1, "y_start_ratio": 0.8, "y_end_ratio": 1},
    "center": {"x_start_ratio": 0.25, "x_end_ratio": 0.75, "y_start_ratio": 0.25, "y_end_ratio": 0.75},
}
# add this to the game configs, and more regions, change the way it gets compared

def get_clip_urls(gameplay_clips, clip_amount):
    return [clip["url"] for clip in gameplay_clips[:clip_amount]]

def get_steamer_names(gameplay_clips, clip_amount):
    return [clip["broadcaster_name"] for clip in gameplay_clips[:clip_amount]]



def get_clip_amount(clip_data, max_duration): 
    amount = 0 
    duration = 0
    for clip in clip_data:
        duration += clip["duration"]  
        amount += 1
        if duration >= max_duration:
            break
    return amount
       




def save_clip_paths(clips_dir):
    paths = sorted(os.listdir(clips_dir))

    with open("clips.txt", "w") as f:
        for name in paths:
            full_path = os.path.abspath(os.path.join(clips_dir, name))
            f.write(f"file '{full_path}'\n") 

import os

def get_clip_paths(folder="clips"):
    files = sorted(os.listdir(folder))
    return [
        os.path.join(folder, f)
        for f in files
        if f.endswith(".mp4")
    ]


def crop_image_region(img, region): 
    h, w, _ = img.shape 
    x1 = int(w * region.get("x_start", 0.0))
    x2 = int(w * region.get("x_end", 1.0))
    y1 = int(h * region.get("y_start", 0.0))
    y2 = int(h * region.get("y_end", 1.0))
            
    return img[x1:x2, y1:y2]