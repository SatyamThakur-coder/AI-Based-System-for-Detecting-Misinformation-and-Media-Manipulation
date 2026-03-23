"""
File upload and handling utilities
"""
import os
import aiofiles
from fastapi import UploadFile
from app.config import settings


async def save_upload_file(upload_file: UploadFile, content_id: int) -> tuple:
    """Save uploaded file and return (path, size)"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    file_extension = os.path.splitext(upload_file.filename)[1]
    filename = f"content_{content_id}_{upload_file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    file_size = 0
    async with aiofiles.open(file_path, "wb") as f:
        while content := await upload_file.read(1024 * 1024):
            await f.write(content)
            file_size += len(content)

    return file_path, file_size


def get_content_type(filename: str) -> str:
    """Determine content type from filename"""
    if not filename:
        return "unknown"
    ext = os.path.splitext(filename)[1].lower()

    image_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"]
    video_exts = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv"]
    audio_exts = [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac", ".wma"]

    if ext in image_exts:
        return "image"
    elif ext in video_exts:
        return "video"
    elif ext in audio_exts:
        return "audio"
    else:
        return "unknown"
