from checks.base import CheckResult, CheckStatus

def check_hold_volume(difficulty):
    notes = difficulty.get("data", {}).get("notes", [])
    holds = [n for n in notes if n.get("type") == "hold"]
    
    if not holds:
        return CheckResult(CheckStatus.PASS, "Hold Volume")
    
    loud_holds = []
    for hold in holds:
        volume = hold.get("hitsound", {}).get("hold", {}).get("volume", 0)
        if volume > 70:
            loud_holds.append(hold)
    
    if loud_holds:
        return CheckResult(
            CheckStatus.WARNING,
            "Hold Volume",
            f"{len(loud_holds)} held note(s) have a hold loop volume over 70. Make sure these are intentional, as they can potientially be unintentionally obnoxious."
        )
    
    return CheckResult(CheckStatus.PASS, "Hold Volume")

