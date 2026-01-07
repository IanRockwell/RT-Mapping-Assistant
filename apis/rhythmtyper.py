import aiohttp
import asyncio
import zipfile
import json
from io import BytesIO
from pprint import pprint
from PIL import Image

async def download_and_analyze_beatmap(map_id: str):
    """Download and analyze a beatmap, keeping everything in memory."""
    url = f"https://storage.googleapis.com/rhythm-typer.firebasestorage.app/beatmaps/{map_id}/{map_id}.rtm"
    
    async with aiohttp.ClientSession() as s, s.get(url) as r:
        if r.status == 403:
            raise Exception(f"Map with id {map_id} does not exist.")
        if r.status != 200:
            raise Exception(f"Failed to download map: HTTP {r.status}")
        
        zip_bytes = BytesIO(await r.read())
    
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

if __name__ == "__main__":
    result = asyncio.run(download_and_analyze_beatmap("bovwxvt4yuke"))
    pprint(result)
