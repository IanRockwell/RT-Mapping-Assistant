import aiohttp
import zipfile
import json
from io import BytesIO
from PIL import Image

def format_length(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

async def fetch_online_beatmap_metadata(map_id: str):

    url = f"https://us-central1-rhythm-typer.cloudfunctions.net/api/getBeatmaps?limit=1&mapsetId={map_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 403:
                raise ValueError(f"Map with id {map_id} does not exist.")
            if resp.status != 200:
                raise RuntimeError(f"Failed to fetch metadata: HTTP {resp.status}")
            return await resp.json()

async def fetch_beatmap(map_id: str) -> BytesIO:

    url = f"https://storage.googleapis.com/rhythm-typer.firebasestorage.app/beatmaps/{map_id}/{map_id}.rtm"
    
    async with aiohttp.ClientSession() as s, s.get(url) as r:
        if r.status == 403:
            raise ValueError(f"Map with id {map_id} does not exist.")
        if r.status != 200:
            raise RuntimeError(f"Failed to download map: HTTP {r.status}")
        
        return BytesIO(await r.read())

def analyze_beatmap(zip_bytes: BytesIO) -> dict:

    result = {
        "meta": None,
        "difficulties": [],
        "background": None,
        "audio": None,
        "video": None,
        "hitsounds": []
    }
    
    with zipfile.ZipFile(zip_bytes, 'r') as z:
        for f in z.namelist():
            info = z.getinfo(f)
            
            if f == "meta.json":
                result["meta"] = json.loads(z.read(f))
            elif f.endswith(".json"):
                result["difficulties"].append({
                    "filename": f,
                    "data": json.loads(z.read(f))
                })
            elif f.lower().endswith((".jpg", ".jpeg", ".png")):
                img_bytes = z.read(f)
                with Image.open(BytesIO(img_bytes)) as img:
                    result["background"] = {
                        "filename": f,
                        "width": img.width,
                        "height": img.height,
                        "size_bytes": info.file_size
                    }
            elif f.lower().endswith((".mp3", ".ogg", ".wav")):
                result["audio"] = {
                    "filename": f,
                    "size_bytes": info.file_size
                }
            elif f.lower().endswith((".mp4", ".webm")):
                result["video"] = {
                    "filename": f,
                    "size_bytes": info.file_size
                }
            elif f.startswith("hitsounds/") and not f.endswith("/"):
                result["hitsounds"].append({
                    "filename": f,
                    "size_bytes": info.file_size
                })
    
    return result

