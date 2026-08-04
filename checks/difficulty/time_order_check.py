from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp


def check_time_order(difficulty, meta=None):
    data = difficulty.get("data", {})
    notes = data.get("notes", [])
    typing_sections = data.get("typingSections", [])

    invalid_holds = []
    for note in notes:
        if note.get("type") == "hold":
            start = note.get("startTime", 0)
            end = note.get("endTime", 0)
            if end <= start:
                invalid_holds.append(note)

    invalid_sections = []
    for section in typing_sections:
        start = section.get("startTime", 0)
        end = section.get("endTime", 0)
        if end <= start:
            invalid_sections.append(section)

    if not invalid_holds and not invalid_sections:
        return CheckResult(CheckStatus.PASS, "Time Order")

    attachment_lines = []

    if invalid_holds:
        formatted = [format_timestamp(h.get("startTime", 0)) for h in invalid_holds]
        attachment_lines.append(f"Invalid Hold Notes ({len(invalid_holds)} total):")
        for i in range(0, len(formatted), 10):
            attachment_lines.append(", ".join(formatted[i : i + 10]))
        attachment_lines.append("")

    if invalid_sections:
        formatted = [format_timestamp(s.get("startTime", 0)) for s in invalid_sections]
        attachment_lines.append(f"Invalid Typing Sections ({len(invalid_sections)} total):")
        for i in range(0, len(formatted), 10):
            attachment_lines.append(", ".join(formatted[i : i + 10]))
        attachment_lines.append("")

    attachment_content = "\n".join(attachment_lines)

    parts = []
    if invalid_holds:
        parts.append(f"{len(invalid_holds)} hold note(s)")
    if invalid_sections:
        parts.append(f"{len(invalid_sections)} typing section(s)")
    listed = " and ".join(parts)

    return CheckResult(
        CheckStatus.FAIL,
        "Time Order",
        f"\n- {listed} have an end time that is not after their start time. See attached file for details.",
        attachment=("invalid_time_order.txt", attachment_content),
    )
