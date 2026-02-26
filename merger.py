import subprocess
import os
import logging

logger = logging.getLogger(__name__)


class Merger:
    def __init__(self, width=1920, height=1080, fps=30, use_hw_accel=True):
        self.width = width
        self.height = height
        self.fps = fps
        self.use_hw_accel = use_hw_accel
    
    def merge_clips(self, clip_paths, streamer_names=None, view_counts=None, output_path=None):
        if not clip_paths:
            logger.warning("No clips to merge.")
            return
        
        if output_path is None:
            raise ValueError("output_path is required")
        
        streamer_names = streamer_names or []
        view_counts = view_counts or []
        
        inputs = []
        filter_parts = []
        
        for i, path in enumerate(clip_paths):
            if not os.path.exists(path):
                logger.warning(f"Clip path not found, skipping: {path}")
                continue
            
            inputs.extend(["-i", path])
            
            streamer = streamer_names[i] if i < len(streamer_names) else 'Unknown'
            views = view_counts[i] if i < len(view_counts) else 0
            
            filter_parts.append(
                f"[{i}:v]scale={self.width}:{self.height}:force_original_aspect_ratio=decrease,"
                f"pad={self.width}:{self.height}:(ow-iw)/2:(oh-ih)/2,fps={self.fps},format=yuv420p,"
                f"drawtext=text='{streamer}':fontsize=48:fontcolor=white:x=10:y=10:box=1:boxcolor=black@0.5:boxborderw=5,"
                f"drawtext=text='Views\\: {views}':fontsize=36:fontcolor=white:x=10:y=h-th-10:box=1:boxcolor=black@0.5:boxborderw=5,"
                f"setpts=PTS-STARTPTS[v{i}];"
                f"[{i}:a]aresample=48000,asetpts=PTS-STARTPTS[a{i}];"
            )
        
        if not filter_parts:
            logger.error("No valid clips found after filtering.")
            return
        
        n = len(filter_parts)
        concat_inputs = "".join(f"[v{i}][a{i}]" for i in range(n))
        filter_complex = "".join(filter_parts) + f"{concat_inputs}concat=n={n}:v=1:a=1[outv][outa]"
        
        cmd = self._build_ffmpeg_command(inputs, filter_complex, output_path)
        
        logger.info(f"Merging {n} clips with FFmpeg")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError("FFmpeg failed")
        else:
            logger.info(f"Merged {n} clips into {output_path}")
    
    def _build_ffmpeg_command(self, inputs, filter_complex, output_path):
        if self.use_hw_accel:
            return [
                "ffmpeg", "-y",
                "-hwaccel", "videotoolbox",
                *inputs,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "[outa]",
                "-c:v", "h264_videotoolbox",
                "-b:v", "8M",
                "-c:a", "aac",
                "-b:a", "192k",
                output_path
            ]
        else:
            return [
                "ffmpeg", "-y",
                *inputs,
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-map", "[outa]",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "23",
                "-threads", "0",
                "-c:a", "aac",
                "-b:a", "192k",
                output_path
            ]