from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp, SNAP_TOLERANCE_MS


def format_range(start, end):
    if start == end:
        return format_timestamp(start)
    return f"{format_timestamp(start)} - {format_timestamp(end)}"


def check_key_overlap(difficulty, meta=None):
    notes = difficulty.get("data", {}).get("notes", [])

    if not notes:
        return CheckResult(CheckStatus.PASS, "Key Overlap")

    notes_by_key = {}
    for note in notes:
        key = note.get("key")
        if key is None:
            continue
        if note.get("type") == "hold":
            start = note.get("startTime", 0)
            end = note.get("endTime", 0)
        else:
            start = note.get("time", 0)
            end = start
        notes_by_key.setdefault(key, []).append((start, end))

    overlaps = []
    for key, intervals in notes_by_key.items():
        intervals.sort()
        active_start, active_end = intervals[0]
        for start, end in intervals[1:]:
            if start - active_end <= SNAP_TOLERANCE_MS:
                overlaps.append((start, key, (start, end), (active_start, active_end)))
                if end > active_end:
                    active_end = end
            else:
                active_start, active_end = start, end

    if not overlaps:
        return CheckResult(CheckStatus.PASS, "Key Overlap")

    overlaps.sort()

    attachment_lines = [f"Same-Key Overlaps ({len(overlaps)} total):"]
    for _, key, current, previous in overlaps:
        attachment_lines.append(
            f"{format_range(*current)} - key '{key}' "
            f"overlaps {format_range(*previous)}"
        )
    attachment_lines.append("")
    attachment_content = "\n".join(attachment_lines)

    return CheckResult(
        CheckStatus.FAIL,
        "Key Overlap",
        (
            f"\n- {len(overlaps)} note(s) share a key with another note that is still active "
            "or placed at the same time. See attached file for details."
        ),
        attachment=("same_key_overlaps.txt", attachment_content),
    )
