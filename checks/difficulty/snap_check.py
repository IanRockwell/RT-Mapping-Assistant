from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp, get_snap_data


def check_unsnapped_notes(difficulty, meta=None):
    _, unsnapped_timestamps = get_snap_data(difficulty, meta)

    if unsnapped_timestamps is None or not unsnapped_timestamps:
        return CheckResult(CheckStatus.PASS, "Snap")

    formatted = [format_timestamp(t) for t in sorted(unsnapped_timestamps)]
    attachment_lines = [f"Unsnapped Notes ({len(unsnapped_timestamps)} total):"]
    for i in range(0, len(formatted), 10):
        attachment_lines.append(", ".join(formatted[i:i + 10]))
    attachment_lines.append("")
    attachment_content = "\n".join(attachment_lines)

    return CheckResult(
        CheckStatus.FAIL,
        "Snap",
        f"{len(unsnapped_timestamps)} note(s) are not snapped to any standard beat division (1/1 through 1/32). See attached file for timestamps.",
        attachment=("unsnapped_notes.txt", attachment_content)
    )

