from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp


def check_hold_volume(difficulty, meta=None):
    notes = difficulty.get("data", {}).get("notes", [])
    holds = [n for n in notes if n.get("type") == "hold"]

    if not holds:
        return CheckResult(CheckStatus.PASS, "Hold")

    loud_holds = []
    for hold in holds:
        volume = hold.get("hitsound", {}).get("hold", {}).get("volume", 0)
        if volume > 60:
            loud_holds.append(hold)

    if not loud_holds:
        return CheckResult(CheckStatus.PASS, "Hold")

    percentage = (len(loud_holds) / len(holds)) * 100

    if percentage > 40:
        return CheckResult(
            CheckStatus.WARNING,
            "Hold",
            (
                f"\n- {percentage:.0f}% of hold note(s) "
                f"({len(loud_holds)}/{len(holds)}) have a hold volume above 60. "
                "It is recommended to only use hold volumes above 60% for good reason."
            ),
        )

    timestamps = sorted(set(h.get("startTime", 0) for h in loud_holds))
    formatted = [format_timestamp(t) for t in timestamps]

    attachment_lines = [
        f"Loud Hold Notes (>60% volume) ({len(loud_holds)} of {len(holds)} hold notes, {percentage:.0f}%):"
    ]
    for i in range(0, len(formatted), 10):
        attachment_lines.append(", ".join(formatted[i : i + 10]))
    attachment_lines.append("")
    attachment_content = "\n".join(attachment_lines)

    return CheckResult(
        CheckStatus.WARNING,
        "Hold",
        (
            f"\n- {len(loud_holds)}/{len(holds)} hold notes have a hold volume above 60%. "
            "Ensure these are intentional. See attached file for details."
        ),
        attachment=("loud_hold_notes.txt", attachment_content),
    )
