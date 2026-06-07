import json
from pathlib import Path

import requests

from lib.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN

_TOKEN_URL = "https://oauth2.googleapis.com/token"
_UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
_CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB


def _access_token() -> str:
    resp = requests.post(_TOKEN_URL, data={
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "refresh_token": YOUTUBE_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }, timeout=30)
    resp.raise_for_status()
    return resp.json()["access_token"]


def upload_video(video_path: Path, title: str, description: str, tags: list,
                 category_id: str = "22", privacy: str = "private",
                 publish_at: str = None) -> str:
    """Upload a video. If publish_at (ISO 8601 UTC) is set, schedules it for that time
    and ignores the privacy arg (YouTube requires privacyStatus=private for scheduling)."""
    video_path = Path(video_path)
    file_size = video_path.stat().st_size
    token = _access_token()

    status = {"privacyStatus": "private" if publish_at else privacy,
              "selfDeclaredMadeForKids": False}
    if publish_at:
        status["publishAt"] = publish_at

    metadata = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
        },
        "status": status,
    }

    # Initiate resumable upload session
    init = requests.post(
        _UPLOAD_URL,
        params={"uploadType": "resumable", "part": "snippet,status"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(file_size),
        },
        json=metadata,
        timeout=30,
    )
    init.raise_for_status()
    session_url = init.headers["Location"]

    # Upload in chunks
    uploaded = 0
    with open(video_path, "rb") as f:
        while uploaded < file_size:
            chunk = f.read(_CHUNK_SIZE)
            chunk_len = len(chunk)
            end_byte = uploaded + chunk_len - 1

            resp = requests.put(
                session_url,
                headers={
                    "Content-Length": str(chunk_len),
                    "Content-Range": f"bytes {uploaded}-{end_byte}/{file_size}",
                },
                data=chunk,
                timeout=120,
            )

            if resp.status_code in (200, 201):
                video_id = resp.json()["id"]
                print(f"  Upload complete: https://youtu.be/{video_id}")
                return video_id
            elif resp.status_code == 308:
                range_header = resp.headers.get("Range", "")
                uploaded = int(range_header.split("-")[1]) + 1 if range_header else uploaded + chunk_len
                pct = uploaded / file_size * 100
                print(f"  Uploading... {pct:.0f}%")
            else:
                resp.raise_for_status()

    raise RuntimeError("Upload finished without receiving a video ID")
