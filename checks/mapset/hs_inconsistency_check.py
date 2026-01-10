from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp

TIME_TOLERANCE_MS = 5


def _normalize_sounds(sounds):
    if not sounds:
        return None
    active = (
        sounds.get("hitclap", False),
        sounds.get("hitwhistle", False),
        sounds.get("hitfinish", False)
    )
    if not any(active):
        return None
    return active


def _extract_note_data(notes):
    all_times = set()
    hitsound_data = {}
    
    for note in notes:
        hitsound = note.get("hitsound")
        
        if note.get("type") == "hold":
            start_time = note.get("startTime")
            end_time = note.get("endTime")
            
            if start_time is not None:
                all_times.add(start_time)
                if hitsound:
                    start = hitsound.get("start", {})
                    normalized = _normalize_sounds(start.get("sounds"))
                    if normalized:
                        hitsound_data[start_time] = normalized
            
            if end_time is not None:
                all_times.add(end_time)
                if hitsound:
                    end = hitsound.get("end", {})
                    normalized = _normalize_sounds(end.get("sounds"))
                    if normalized:
                        hitsound_data[end_time] = normalized
        else:
            note_time = note.get("time")
            if note_time is not None:
                all_times.add(note_time)
                if hitsound:
                    normalized = _normalize_sounds(hitsound.get("sounds"))
                    if normalized:
                        hitsound_data[note_time] = normalized
    
    return all_times, hitsound_data


def _find_closest_match(times_set, target_time, tolerance=TIME_TOLERANCE_MS):
    if target_time is None:
        return None
    for t in times_set:
        if t is not None and abs(t - target_time) <= tolerance:
            return t
    return None


def _get_hitsound_at_time(hitsound_data, target_time, tolerance=TIME_TOLERANCE_MS):
    for t, sounds in hitsound_data.items():
        if t is not None and abs(t - target_time) <= tolerance:
            return sounds
    return None


def check_hitsound_consistency(result):
    difficulties = result.get("difficulties", [])
    
    if len(difficulties) < 2:
        return CheckResult(CheckStatus.PASS, "HS Inconsistency")
    
    diff_data = {}
    for diff in difficulties:
        data = diff.get("data", {})
        name = data.get("name", diff.get("filename", "Unknown"))
        notes = data.get("notes", [])
        all_times, hitsound_data = _extract_note_data(notes)
        diff_data[name] = {
            "all_times": all_times,
            "hitsound_data": hitsound_data
        }
    
    inconsistencies = []
    diff_names = list(diff_data.keys())
    
    for i, diff1_name in enumerate(diff_names):
        for diff2_name in diff_names[i + 1:]:
            diff1 = diff_data[diff1_name]
            diff2 = diff_data[diff2_name]
            
            mismatched_times = set()
            
            for t in diff1["hitsound_data"]:
                if t is None:
                    continue
                matched_time = _find_closest_match(diff2["all_times"], t)
                if matched_time is not None:
                    diff1_sounds = diff1["hitsound_data"].get(t)
                    diff2_sounds = _get_hitsound_at_time(diff2["hitsound_data"], t)
                    if diff1_sounds != diff2_sounds:
                        mismatched_times.add(t)
            
            for t in diff2["hitsound_data"]:
                if t is None:
                    continue
                matched_time = _find_closest_match(diff1["all_times"], t)
                if matched_time is not None:
                    diff2_sounds = diff2["hitsound_data"].get(t)
                    diff1_sounds = _get_hitsound_at_time(diff1["hitsound_data"], t)
                    if diff1_sounds != diff2_sounds:
                        mismatched_times.add(t)
            
            if mismatched_times:
                inconsistencies.append({
                    "diff1": diff1_name,
                    "diff2": diff2_name,
                    "times": sorted(mismatched_times)
                })
    
    if not inconsistencies:
        return CheckResult(CheckStatus.PASS, "HS Inconsistency")
    
    # Build the attachment content with all differences
    attachment_lines = []
    for inc in inconsistencies:
        times = inc["times"]
        formatted = [format_timestamp(t) for t in times]
        attachment_lines.append(f"Hitsound differences between '{inc['diff1']}' and '{inc['diff2']}' ({len(times)} total):")
        for i in range(0, len(formatted), 10):
            attachment_lines.append(", ".join(formatted[i:i + 10]))
        attachment_lines.append("")
    
    attachment_content = "\n".join(attachment_lines)
    
    # Build summary message
    messages = ["Ensure these are intentional. If they're not, consider using __/copyhitsounds__ to make them consistent."]
    for inc in inconsistencies[:5]:  # Limit to 5 messages
        times = inc["times"]
        messages.append(
            f"- '{inc['diff1']}' and '{inc['diff2']}' have mismatched hitsounds ({len(times)} differences)"
        )
    
    if len(inconsistencies) > 5:
        messages.append("- etc.")
    
    return CheckResult(
        CheckStatus.WARNING,
        "HS Inconsistency",
        "\n".join(messages),
        attachment=("hitsound_differences.txt", attachment_content)
    )
