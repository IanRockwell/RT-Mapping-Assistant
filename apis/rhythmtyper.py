import aiohttp
import zipfile
import json
from io import BytesIO
from PIL import Image
from mutagen import File as MutagenFile

def format_length(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def format_timestamp(ms):
    total_seconds = ms / 1000
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    centiseconds = int((ms % 1000) / 10)
    return f"{minutes}:{seconds:02d}:{centiseconds:02d}"

async def fetch_online_beatmap_metadata(map_id):

    url = f"https://us-central1-rhythm-typer.cloudfunctions.net/api/getBeatmaps?limit=1&mapsetId={map_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 403:
                raise ValueError(f"Map with id {map_id} does not exist.")
            if resp.status != 200:
                raise RuntimeError(f"Failed to fetch metadata: HTTP {resp.status}")
            return await resp.json()

async def fetch_beatmap(map_id):

    url = f"https://storage.googleapis.com/rhythm-typer.firebasestorage.app/beatmaps/{map_id}/{map_id}.rtm"
    
    async with aiohttp.ClientSession() as s, s.get(url) as r:
        if r.status == 403:
            raise ValueError(f"Map with id {map_id} does not exist.")
        if r.status != 200:
            raise RuntimeError(f"Failed to download map: HTTP {r.status}")
        
        return BytesIO(await r.read())

def analyze_beatmap(zip_bytes):

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
            elif f.lower().startswith("audio.") and f.lower().endswith((".mp3", ".ogg", ".wav")):
                audio_bytes = BytesIO(z.read(f))
                audio_file = MutagenFile(audio_bytes)
                duration = audio_file.info.length if audio_file and audio_file.info else None
                
                bitrate = None
                if duration and duration > 0:
                    bits = info.file_size * 8
                    bitrate = (bits / duration) / 1000  # kbps
                
                result["audio"] = {
                    "filename": f,
                    "size_bytes": info.file_size,
                    "duration": duration,
                    "bitrate": round(bitrate, 1) if bitrate else None
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

def calculate_drain_time(difficulty):
    data = difficulty.get("data", {})
    notes = data.get("notes", [])
    typing_sections = data.get("typingSections", [])
    
    if not notes and not typing_sections:
        return 0
    
    # Collect all event times (notes and typing sections)
    event_times = []
    
    for note in notes:
        if note.get("type") == "hold":
            event_times.append(note.get("startTime", 0))
            event_times.append(note.get("endTime", 0))
        else:
            event_times.append(note.get("time", 0))
    
    for section in typing_sections:
        event_times.append(section.get("startTime", 0))
        event_times.append(section.get("endTime", 0))

    event_times.sort()
    
    if len(event_times) < 2:
        return 0
    
    first_event = event_times[0]
    last_event = event_times[-1]
    drain_length = last_event - first_event
    
    gap_threshold = 5000
    
    for i in range(1, len(event_times)):
        gap = event_times[i] - event_times[i - 1]
        if gap >= gap_threshold:
            drain_length -= gap
    
    return max(drain_length, 0)
