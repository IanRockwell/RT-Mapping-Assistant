import aiohttp
import zipfile
import json
import re
from io import BytesIO
from PIL import Image
from tinytag import TinyTag


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

def extract_beatmap_id_from_url(url):
    match = re.search(r"(?:rhythmtyper\.net|rhythm-typer\.web\.app|rhythm-typer\.webapp|rhythm\-typer\.web\.app|rhythm-typer\.webapp|rhythm-typer\.web\.app|rhythm-typer\.web\.app|rhythm-typer\.webapp|rhythmtyper\.web\.app|rhythmtyper\.webapp)/beatmap/([a-zA-Z0-9]+)", url)
    if not match:
        match = re.search(r"(?:rhythmtyper\.net|rhythmtyper\.web\.app)/beatmap/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

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

    url = f"https://storage.googleapis.com/rhythm-typer.firebasestorage.app/beatmaps/{map_id}/{map_id}.rtm?=v#"
    
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
        namelist = z.namelist()
        if "meta.json" in namelist:
            result["meta"] = json.loads(z.read("meta.json"))

        for f in namelist:
            info = z.getinfo(f)
            audio_file_meta = (result.get("meta") or {}).get("audioFile")
            is_audio = (audio_file_meta and f.lower() == audio_file_meta.lower()) or (
                not audio_file_meta and f.lower().startswith("audio.") and f.lower().endswith((".mp3", ".ogg", ".wav"))
            )

            if f == "meta.json":
                pass
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
            elif is_audio:
                audio_bytes = BytesIO(z.read(f))
                audio_bytes.seek(0)
                try:
                    tag = TinyTag.get(file_obj=audio_bytes)
                    duration = tag.duration if tag else None
                    bitrate = tag.bitrate if tag and tag.bitrate else None
                except Exception:
                    duration = None
                    bitrate = None
                if bitrate is None and duration and duration > 0:
                    bitrate = (info.file_size * 8 / duration) / 1000

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


def get_timing_points(meta):
    timing_points = (meta or {}).get("timingPoints", [])
    for tp in timing_points:
        tp["offset"] = int(round(tp.get("time", 0) * 1000))
    return sorted(timing_points, key=lambda tp: tp["offset"])


def get_timing_point(time_ms, timing_points):
    applicable = timing_points[0]
    for tp in timing_points:
        if tp["offset"] <= time_ms:
            applicable = tp
        else:
            break
    return applicable


def get_snap_division(note_time, tp, divisors, snap_tolerance_ms):
    bpm = tp.get("bpm", 120)
    offset = tp.get("offset", 0)
    ms_per_beat = 60000 / bpm
    relative_pos = note_time - offset

    for div in divisors:
        snap_interval = ms_per_beat / div
        remainder = relative_pos % snap_interval
        distance = min(remainder, snap_interval - remainder)

        if distance <= snap_tolerance_ms:
            return f"1/{div}"

    return "unsnapped"


def get_snap_data(difficulty, meta=None):

    timing_points = get_timing_points(meta)

    data = difficulty.get("data", {})
    notes = data.get("notes", [])

    counts = {
        "1/1": 0, "1/2": 0, "1/3": 0, "1/4": 0, "1/5": 0, "1/6": 0,
        "1/7": 0, "1/8": 0, "1/12": 0, "1/16": 0, "1/32": 0,
        "unsnapped": 0
    }

    if not notes:
        return (counts, [], {})

    snap_tolerance_ms = 2
    divisors = [1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 32]

    unsnapped_timestamps = []
    timestamps_by_division = {}

    for note in notes:
        if note.get("type") == "hold":
            times_to_check = [note.get("startTime", 0), note.get("endTime", 0)]
        else:
            times_to_check = [note.get("time", 0)]

        for note_time in times_to_check:
            tp = get_timing_point(note_time, timing_points)
            snap = get_snap_division(note_time, tp, divisors, snap_tolerance_ms)
            counts[snap] = counts.get(snap, 0) + 1
            if snap not in timestamps_by_division:
                timestamps_by_division[snap] = []
            timestamps_by_division[snap].append(note_time)
            if snap == "unsnapped":
                unsnapped_timestamps.append(note_time)

    return (counts, unsnapped_timestamps, timestamps_by_division)


def calculate_snap_counts(difficulty, meta=None):
    counts, _, _ = get_snap_data(difficulty, meta)
    return counts


def calculate_drain_time(difficulty):
    data = difficulty.get("data", {})
    notes = data.get("notes", [])
    typing_sections = data.get("typingSections", [])
    
    if not notes and not typing_sections:
        return 0
    
    event_times = []
    
    for note in notes:
        if note.get("type") == "hold":
            event_times.append(note.get("startTime", 0))
            event_times.append(note.get("endTime", 0))
        else:
            event_times.append(note.get("time", 0))

    event_times.sort()
    
    drain_length = 0
    if len(event_times) >= 2:
        first_event = event_times[0]
        last_event = event_times[-1]
        drain_length = last_event - first_event
        
        gap_threshold = 5000
        
        for i in range(1, len(event_times)):
            gap = event_times[i] - event_times[i - 1]
            if gap >= gap_threshold:
                drain_length -= gap
    
    for section in typing_sections:
        start = section.get("startTime", 0)
        end = section.get("endTime", 0)
        drain_length += end - start
    
    return max(drain_length, 0)
