import subprocess
import os
from config import GAME_NAME

def merge_clips(clip_paths, streamer_names=[], output=f"{GAME_NAME}.mp4", width=1920, height=1080, fps=30):
    if not clip_paths:
        print("No clips to merge.")
        return

    inputs = []
    filter_parts = []
    valid_index = 0

    for i, path in enumerate(clip_paths):
        if not os.path.exists(path):
            print(f"Warning: {path} not found, skipping.")
            continue


        inputs.extend(["-i", path])
        filter_parts.append(
            f"[{i}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps={fps},format=yuv420p,"
            f"setpts=PTS-STARTPTS[v{i}];"
            f"[{i}:a]aresample=48000,asetpts=PTS-STARTPTS[a{i}];"
        )
        valid_index += 1

    if not filter_parts:
        print("No valid clips found.")
        return

    n = len(filter_parts)
    concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(n))
    filter_complex = "".join(filter_parts) + f"{concat_inputs}concat=n={n}:v=1:a=1[outv][outa]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        output
    ]

    print("Running FFmpeg command...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("FFmpeg stderr:\n", result.stderr)
        raise RuntimeError("FFmpeg failed")
    else:
        print(f"Merged {n} clips into {output}")