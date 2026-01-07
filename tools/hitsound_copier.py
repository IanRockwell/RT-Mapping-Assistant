import json
import zipfile
from io import BytesIO


class HitsoundCopyError(Exception):
    pass


TIME_TOLERANCE_MS = 5


def _extract_sound_events(notes):
    events = []
    
    for note in notes:
        hitsound = note.get("hitsound")
        if not hitsound:
            continue
        
        sample_set = hitsound.get("sampleSet", "normal")
        
        if note.get("type") == "hold":
            start = hitsound.get("start", {})
            hold = hitsound.get("hold")
            if start.get("sounds"):
                events.append((
                    note.get("startTime"),
                    start.get("sounds"),
                    start.get("volume", 100),
                    sample_set,
                    hold
                ))
            
            end = hitsound.get("end", {})
            if end.get("sounds"):
                events.append((
                    note.get("endTime"),
                    end.get("sounds"),
                    end.get("volume", 100),
                    sample_set,
                    None
                ))
        else:
            if hitsound.get("sounds"):
                events.append((
                    note.get("time"),
                    hitsound.get("sounds"),
                    hitsound.get("volume", 100),
                    sample_set,
                    None
                ))
    
    events.sort(key=lambda x: x[0] if x[0] is not None else 0)
    return events


def _find_closest_event(events, target_time, tolerance=TIME_TOLERANCE_MS):
    if not events or target_time is None:
        return None
    
    closest = None
    closest_diff = float('inf')
    
    for time, sounds, volume, sample_set, hold_data in events:
        if time is None:
            continue
        diff = abs(time - target_time)
        if diff <= tolerance and diff < closest_diff:
            closest = (sounds, volume, sample_set, hold_data)
            closest_diff = diff
    
    return closest


def copy_hitsounds(zip_bytes, source_difficulty_name):
    try:
        with zipfile.ZipFile(zip_bytes, 'r') as z:
            meta = None
            difficulties = {}
            other_files = {}
            
            for f in z.namelist():
                if f == "meta.json":
                    meta = json.loads(z.read(f))
                elif f.endswith(".json"):
                    difficulties[f] = json.loads(z.read(f))
                else:
                    other_files[f] = z.read(f)
            
            if not meta:
                raise HitsoundCopyError("Invalid RTM file: missing meta.json")
            
            source_diff = None
            source_filename = None
            for filename, diff_data in difficulties.items():
                if diff_data.get("name", "").lower() == source_difficulty_name.lower():
                    source_diff = diff_data
                    source_filename = filename
                    break
            
            if not source_diff:
                diff_names = [d.get("name", "Unknown") for d in difficulties.values()]
                raise HitsoundCopyError(
                    f"Difficulty '{source_difficulty_name}' not found. "
                    f"Available difficulties: {', '.join(diff_names)}"
                )
            
            source_events = _extract_sound_events(source_diff.get("notes", []))
            
            modified_count = 0
            for filename, diff_data in difficulties.items():
                if filename == source_filename:
                    continue
                
                for note in diff_data.get("notes", []):
                    if note.get("type") == "hold":
                        start_time = note.get("startTime")
                        end_time = note.get("endTime")
                        
                        start_match = _find_closest_event(source_events, start_time)
                        end_match = _find_closest_event(source_events, end_time)
                        
                        if start_match or end_match:
                            if "hitsound" not in note:
                                note["hitsound"] = {}
                            
                            hitsound = note["hitsound"]
                            
                            if start_match:
                                sounds, volume, sample_set, hold_data = start_match
                                hitsound["sampleSet"] = sample_set
                                hitsound["start"] = {
                                    "volume": volume,
                                    "sounds": sounds.copy()
                                }
                                if hold_data:
                                    hitsound["hold"] = hold_data.copy()
                                modified_count += 1
                            
                            if end_match:
                                sounds, volume, sample_set, _ = end_match
                                hitsound["sampleSet"] = sample_set
                                hitsound["end"] = {
                                    "volume": volume,
                                    "sounds": sounds.copy()
                                }
                                modified_count += 1
                    else:
                        tap_time = note.get("time")
                        match = _find_closest_event(source_events, tap_time)
                        
                        if match:
                            sounds, volume, sample_set, _ = match
                            note["hitsound"] = {
                                "sampleSet": sample_set,
                                "volume": volume,
                                "sounds": sounds.copy()
                            }
                            modified_count += 1
            
            output_buffer = BytesIO()
            with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as out_zip:
                out_zip.writestr("meta.json", json.dumps(meta, indent=2))
                
                for filename, diff_data in difficulties.items():
                    out_zip.writestr(filename, json.dumps(diff_data, indent=2))
                
                for filename, data in other_files.items():
                    out_zip.writestr(filename, data)
            
            output_buffer.seek(0)
            
            return output_buffer, {
                "modified_notes": modified_count,
                "target_difficulties": len(difficulties) - 1,
                "source_name": source_diff.get("name")
            }
            
    except zipfile.BadZipFile:
        raise HitsoundCopyError("Invalid RTM file: not a valid zip archive")
    except json.JSONDecodeError:
        raise HitsoundCopyError("Invalid RTM file: contains malformed JSON")
