from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp, SNAP_TOLERANCE_MS


def check_chord_alignment(difficulty, meta=None):
    notes = difficulty.get("data", {}).get("notes", [])

    if not notes:
        return CheckResult(CheckStatus.PASS, "Chord Alignment")

    keys_by_time = {}
    for note in notes:
        if note.get("type") == "hold":
            note_times = [note.get("startTime", 0), note.get("endTime", 0)]
        else:
            note_times = [note.get("time", 0)]

        for note_time in note_times:
            keys_by_time.setdefault(note_time, set()).add(note.get("key"))

    sorted_times = sorted(keys_by_time)

    groups = []
    current = [sorted_times[0]]
    for time in sorted_times[1:]:
        if time - current[-1] <= SNAP_TOLERANCE_MS:
            current.append(time)
        else:
            if len(current) > 1:
                groups.append(current)
            current = [time]
    if len(current) > 1:
        groups.append(current)

    if not groups:
        return CheckResult(CheckStatus.PASS, "Chord Alignment")

    attachment_lines = [f"Misaligned Chords ({len(groups)} total):"]
    for group in groups:
        entries = []
        for t in group:
            keys = sorted(k for k in keys_by_time[t] if k is not None)
            entries.append(f"{format_timestamp(t)} [{', '.join(keys)}]")
        attachment_lines.append(" | ".join(entries))
    attachment_lines.append("")
    attachment_content = "\n".join(attachment_lines)

    return CheckResult(
        CheckStatus.FAIL,
        "Chord Alignment",
        (
            f"\n- {len(groups)} chord(s) have notes within {SNAP_TOLERANCE_MS}ms of each other "
            "without being exactly aligned. See attached file for details."
        ),
        attachment=("misaligned_chords.txt", attachment_content),
    )
