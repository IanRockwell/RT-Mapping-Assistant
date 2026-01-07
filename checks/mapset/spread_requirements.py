from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import calculate_drain_time, format_length

def check_spread_requirements(result):
    difficulties = result.get("difficulties", [])

    if not difficulties:
        return CheckResult(CheckStatus.PASS, "Spread Requirements")
    
    drain_times = [calculate_drain_time(diff) for diff in difficulties]
    shortest_drain = min(drain_times) if drain_times else 0
    shortest_seconds = shortest_drain / 1000
    
    formatted_length = format_length(shortest_seconds)
    
    if shortest_seconds < 30:
        return CheckResult(
            CheckStatus.FAIL,
            "Spread Requirements",
            f"Shortest difficulty is less than 30 seconds. ({formatted_length})"
        )
    
    if shortest_seconds < 90:
        return CheckResult(
            CheckStatus.INFO,
            "Spread Requirements",
            f"Shortest difficulty is {formatted_length}. Ensure you have at least a Normal difficulty, and all in-between difficulties."
        )
    elif shortest_seconds < 135:
        return CheckResult(
            CheckStatus.INFO,
            "Spread Requirements",
            f"Shortest difficulty is {formatted_length}. Ensure you have at least a Hard difficulty, and all in-between difficulties."
        )
    elif shortest_seconds < 180:
        return CheckResult(
            CheckStatus.INFO,
            "Spread Requirements",
            f"Shortest difficulty is {formatted_length}. Ensure you have at least an Insane difficulty, and all in-between difficulties."
        )
    
    return CheckResult(CheckStatus.PASS, "Spread Requirements")

