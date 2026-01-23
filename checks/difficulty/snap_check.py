from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp


def check_unsnapped_notes(difficulty, meta=None):
    if not meta:
        return CheckResult(CheckStatus.PASS, "Snap")
    
    timing_points = meta.get("timingPoints", [])
    if not timing_points:
        return CheckResult(CheckStatus.PASS, "Snap")
    
    timing_points = sorted(timing_points, key=lambda tp: tp.get("offset", 0))
    
    data = difficulty.get("data", {})
    notes = data.get("notes", [])
    
    if not notes:
        return CheckResult(CheckStatus.PASS, "Snap")
    
    snap_tolerance_ms = 2
    divisors = [1, 2, 3, 4, 6, 8, 12, 16]
    
    def get_timing_point(time_ms):
        applicable = timing_points[0]
        for tp in timing_points:
            if tp.get("offset", 0) <= time_ms:
                applicable = tp
            else:
                break
        return applicable
    
    def is_snapped(note_time, tp):
        bpm = tp.get("bpm", 120)
        offset = tp.get("offset", 0)
        ms_per_beat = 60000 / bpm
        
        relative_pos = note_time - offset
        
        for div in divisors:
            snap_interval = ms_per_beat / div
            remainder = relative_pos % snap_interval
            distance = min(remainder, snap_interval - remainder)
            
            if distance <= snap_tolerance_ms:
                return True
        
        return False
    
    unsnapped_notes = []
    
    for note in notes:
        times_to_check = []
        
        if note.get("type") == "hold":
            times_to_check.append(note.get("startTime", 0))
            times_to_check.append(note.get("endTime", 0))
        else:
            times_to_check.append(note.get("time", 0))
        
        for note_time in times_to_check:
            tp = get_timing_point(note_time)
            if not is_snapped(note_time, tp):
                unsnapped_notes.append(note_time)
    
    if unsnapped_notes:
        formatted = [format_timestamp(t) for t in sorted(unsnapped_notes)]
        attachment_lines = [f"Unsnapped Notes ({len(unsnapped_notes)} total):"]
        for i in range(0, len(formatted), 10):
            attachment_lines.append(", ".join(formatted[i:i + 10]))
        attachment_lines.append("")
        attachment_content = "\n".join(attachment_lines)
        
        return CheckResult(
            CheckStatus.FAIL,
            "Snap",
            f"{len(unsnapped_notes)} note(s) are not snapped to any standard beat division (1/1 through 1/16). See attached file for timestamps.",
            attachment=("unsnapped_notes.txt", attachment_content)
        )
    
    return CheckResult(CheckStatus.PASS, "Snap")

