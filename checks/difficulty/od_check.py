from checks.base import CheckResult, CheckStatus


def check_od(difficulty):
    od = difficulty.get("data", {}).get("overallDifficulty", 0)
    
    if od == 0:
        return CheckResult(
            CheckStatus.FAIL,
            "OD",
            "OD has not been set."
        )
    
    if od < 2:
        return CheckResult(
            CheckStatus.WARNING,
            "OD",
            f"OD is low ({od}). Ensure this makes sense."
        )
    
    if od > 8:
        return CheckResult(
            CheckStatus.WARNING,
            "OD",
            f"OD is high ({od}). Ensure this makes sense."
        )
    
    return CheckResult(
        CheckStatus.PASS,
        "OD",
        f"OD is set to {od}."
    )

