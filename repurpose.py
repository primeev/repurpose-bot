import os
import random
import subprocess
import uuid

def random_filters():
    zoom = round(random.uniform(1.00, 1.07), 3)
    bright = round(random.uniform(-0.05, 0.05), 3)
    sat = round(random.uniform(0.9, 1.1), 3)
    speed = round(random.uniform(0.98, 1.02), 3)
    vf = f"scale=iw*{zoom}:ih*{zoom},eq=brightness={bright}:saturation={sat},format=yuv420p"
    return vf, speed

def make_variations(input_path, num_variations=20, out_dir="/tmp/output"):
    os.makedirs(out_dir, exist_ok=True)
    outs = []

    for _ in range(num_variations):
        vf, speed = random_filters()
        out_path = os.path.join(out_dir, f"{uuid.uuid4()}.mp4")

        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-vf", vf,
            "-filter:a", f"atempo={speed}",
            "-crf", "24", "-preset", "superfast",
            "-movflags", "+faststart",
            out_path
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        outs.append(out_path)

    return outs
