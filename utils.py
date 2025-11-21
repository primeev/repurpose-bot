import os
import subprocess
import uuid

async def download_video(msg, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{uuid.uuid4()}.mp4")

    if msg.video:
        f = await msg.video.get_file()
        await f.download_to_drive(out_path)
        return out_path

    if msg.document and (msg.document.mime_type or "").startswith("video"):
        f = await msg.document.get_file()
        await f.download_to_drive(out_path)
        return out_path

    text = (msg.text or "").strip()
    if not text:
        raise ValueError("No video or URL provided")

    subprocess.run(["yt-dlp", "-o", out_path, text], check=True)
    return out_path
