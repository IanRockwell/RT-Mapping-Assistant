from checks.base import CheckResult, CheckStatus

def check_key_count(difficulty):
    notes = difficulty.get("data", {}).get("notes", [])
    
    if not notes:
        return CheckResult(CheckStatus.PASS, "Key Count")
    
    taps = [n for n in notes if n.get("type") == "tap"]
    holds = [n for n in notes if n.get("type") == "hold"]
    
    timestamps = set()
    for n in taps:
        timestamps.add(n.get("time", 0))
    for n in holds:
        timestamps.add(n.get("startTime", 0))
        timestamps.add(n.get("endTime", 0))
    
    for t in timestamps:
        count = 0
        count += sum(1 for n in taps if n.get("time") == t)
        count += sum(1 for n in holds if n.get("startTime", 0) <= t <= n.get("endTime", 0))
        
        if count > 10:
            return CheckResult(
                CheckStatus.FAIL,
                "Key Count",
                f"More than 10 keys pressed at {t}ms ({count} keys)."
            )
    
    return CheckResult(CheckStatus.PASS, "Key Count")

