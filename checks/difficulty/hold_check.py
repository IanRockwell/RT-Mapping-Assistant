from checks.base import CheckResult, CheckStatus


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

    # Only warn if at least 50% of holds are above 60% volume
    if loud_holds and (len(loud_holds) / len(holds)) >= 0.5:
        percentage = (len(loud_holds) / len(holds)) * 100
        return CheckResult(
            CheckStatus.WARNING,
            "Hold",
            (
                f"\n- {percentage:.0f}% of hold note(s) "
                f"({len(loud_holds)}/{len(holds)}) have a hold loop volume above 60. "
                "It is recommended to only use hold volumes above 60% for good reason."
            ),
        )

    return CheckResult(CheckStatus.PASS, "Hold")
