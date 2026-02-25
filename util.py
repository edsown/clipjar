import os

def get_clip_amount(clip_data, max_duration): 
    amount = 0 
    duration = 0
    for clip in clip_data:
        duration += clip["duration"]  
        if duration >= max_duration:
            break
        amount += 1
    return amount
       

def save_clip_paths(clips_dir):
    paths = sorted(os.listdir(clips_dir))

    with open("clips.txt", "w") as f:
        for name in paths:
            full_path = os.path.abspath(os.path.join(clips_dir, name))
            f.write(f"file '{full_path}'\n") 


def get_clip_paths(folder="clips"):
    files = sorted(os.listdir(folder))
    return [
        os.path.join(folder, f)
        for f in files
        if f.endswith(".mp4")
    ]

