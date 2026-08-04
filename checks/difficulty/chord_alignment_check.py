from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp, SNAP_TOLERANCE_MS


def check_chord_alignment(difficulty, meta=None):
    notes = difficulty.get("data", {}).get("notes", [])

    if not notes:
        return CheckResult(CheckStatus.PASS, "Chord Alignment")

    times = set()
    for note in notes:
        if note.get("type") == "hold":
            times.add(note.get("startTime", 0))
            times.add(note.get("endTime", 0))
        else:
            times.add(note.get("time", 0))

    sorted_times = sorted(times)

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
        attachment_lines.append(", ".join(format_timestamp(t) for t in group))
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
