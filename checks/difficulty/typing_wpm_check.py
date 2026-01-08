from checks.base import CheckResult, CheckStatus


def calculate_wpm(text, duration_ms):
    if duration_ms <= 0:
        return float('inf')
    
    characters = len(text)
    duration_minutes = duration_ms / 60000
    wpm = (characters / 5) / duration_minutes
    return wpm


def check_typing_wpm(difficulty):
    data = difficulty.get("data", {})
    typing_sections = data.get("typingSections", [])
    
    if not typing_sections:
        return CheckResult(CheckStatus.PASS, "Typing WPM")
    
    high_wpm_sections = []
    
    for section in typing_sections:
        start_time = section.get("startTime", 0)
        end_time = section.get("endTime", 0)
        text = section.get("text", "")
        
        duration_ms = end_time - start_time
        wpm = calculate_wpm(text, duration_ms)
        
        if wpm > 80:
            high_wpm_sections.append({
                "text": text,
                "wpm": round(wpm, 1),
                "start_time": start_time
            })
    
    if high_wpm_sections:
        details = ", ".join(
            f'"{s["text"]}" ({s["wpm"]} WPM)'
            for s in high_wpm_sections
        )
        return CheckResult(
            CheckStatus.WARNING,
            "Typing WPM",
            f"Typing section(s) requires more than 80 WPM which is quite fast. Ensure this makes sense: {details}"
        )
    
    return CheckResult(CheckStatus.PASS, "Typing WPM")

