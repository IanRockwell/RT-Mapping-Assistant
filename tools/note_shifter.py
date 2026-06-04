import json
import zipfile
from io import BytesIO


def _shift_note_times(note, offset_ms):
    if note.get("type") == "hold":
        if note.get("startTime") is not None:
            note["startTime"] += offset_ms
        if note.get("endTime") is not None:
            note["endTime"] += offset_ms
    else:
        if note.get("time") is not None:
            note["time"] += offset_ms


def offset_notes(zip_bytes, offset_ms, difficulty_names=None):
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
                raise ValueError("Invalid RTM file: missing meta.json")

            # Resolve which difficulties to process
            if difficulty_names:
                canonical = [n.lower() for n in difficulty_names]
                targets = {
                    filename: diff_data
                    for filename, diff_data in difficulties.items()
                    if diff_data.get("name", "").lower() in canonical
                }
                unmatched = set(canonical) - {
                    d.get("name", "").lower() for d in targets.values()
                }
                if unmatched:
                    all_names = [d.get("name", "Unknown") for d in difficulties.values()]
                    raise ValueError(
                        f"Difficulty not found: {', '.join(unmatched)}. "
                        f"Available difficulties: {', '.join(all_names)}"
                    )
            else:
                targets = difficulties

            modified_count = 0
            for filename, diff_data in targets.items():
                for note in diff_data.get("notes", []):
                    _shift_note_times(note, offset_ms)
                    modified_count += 1
                difficulties[filename] = diff_data

            output_buffer = BytesIO()
            with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as out_zip:
                out_zip.writestr("meta.json", json.dumps(meta, indent=2))

                for filename, diff_data in difficulties.items():
                    out_zip.writestr(filename, json.dumps(diff_data, indent=2))

                for filename, data in other_files.items():
                    out_zip.writestr(filename, data)

            output_buffer.seek(0)

            return output_buffer, {
                "shifted_notes": modified_count,
                "difficulties_modified": len(targets),
                "offset_ms": offset_ms
            }

    except zipfile.BadZipFile:
        raise ValueError("Invalid RTM file: not a valid zip archive")
    except json.JSONDecodeError:
        raise ValueError("Invalid RTM file: contains malformed JSON")
