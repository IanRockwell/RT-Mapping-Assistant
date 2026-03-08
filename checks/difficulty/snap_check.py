from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp, get_snap_data

UNCOMMON_SNAP_DIVISIONS = ["1/5", "1/7", "1/12", "1/16", "1/32"]


def check_unsnapped_notes(difficulty, meta=None):
    counts, unsnapped_timestamps, timestamps_by_division = get_snap_data(difficulty, meta)

    if counts is None:
        return CheckResult(CheckStatus.PASS, "Snap")

    if unsnapped_timestamps:
        formatted = [format_timestamp(t) for t in sorted(unsnapped_timestamps)]
        attachment_lines = [f"Unsnapped Notes ({len(unsnapped_timestamps)} total):"]
        for i in range(0, len(formatted), 10):
            attachment_lines.append(", ".join(formatted[i:i + 10]))
        attachment_lines.append("")
        attachment_content = "\n".join(attachment_lines)

        return CheckResult(
            CheckStatus.FAIL,
            "Snap",
            f"\n- {len(unsnapped_timestamps)} note(s) are not snapped to any standard beat division (1/1 through 1/32). See attached file for timestamps.",
            attachment=("unsnapped_notes.txt", attachment_content)
        )

    uncommon_used = [(div, counts.get(div, 0)) for div in UNCOMMON_SNAP_DIVISIONS if counts.get(div, 0) > 0]
    if uncommon_used:
        attachment_lines = []
        for div, count in uncommon_used:
            timestamps = sorted(timestamps_by_division.get(div, []))
            formatted = [format_timestamp(t) for t in timestamps]
            attachment_lines.append(f"{div} ({count} total):")
            for i in range(0, len(formatted), 10):
                attachment_lines.append(", ".join(formatted[i:i + 10]))
            attachment_lines.append("")
        attachment_content = "\n".join(attachment_lines)

        return CheckResult(
            CheckStatus.WARNING,
            "Snap",
            "\n- Map uses uncommon snap divisions (1/5, 1/7, 1/12, 1/16, 1/32). See attached file. Ensure these are intentional.",
            attachment=("uncommon_snap_divisions.txt", attachment_content)
        )

    return CheckResult(CheckStatus.PASS, "Snap")

