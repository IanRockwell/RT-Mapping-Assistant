from checks.base import CheckResult, CheckStatus


def check_has_notes(difficulty):
    notes = difficulty.get("data", {}).get("notes", [])
    
    if not notes:
        return CheckResult(
            CheckStatus.FAIL,
            "Notes",
            "This difficulty has no notes placed."
        )
    
    return CheckResult(
        CheckStatus.PASS,
        "Notes"
    )
