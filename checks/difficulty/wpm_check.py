from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import format_timestamp


def calculate_wpm(text, duration_ms):
    if duration_ms <= 0:
        return float('inf')
    
    characters = len(text)
    duration_minutes = duration_ms / 60000
    wpm = (characters / 5) / duration_minutes
    return wpm


def check_typing_wpm(difficulty, meta=None):
    data = difficulty.get("data", {})
    typing_sections = data.get("typingSections", [])
    
    if not typing_sections:
        return CheckResult(CheckStatus.PASS, "WPM")
    
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
        attachment_lines = [f"High WPM Typing Sections ({len(high_wpm_sections)} total):", ""]
        for s in high_wpm_sections:
            attachment_lines.append(f"[{format_timestamp(s['start_time'])}] {s['wpm']} WPM: \"{s['text']}\"")
        attachment_content = "\n".join(attachment_lines)
        
        return CheckResult(
            CheckStatus.WARNING,
            "WPM",
            f"{len(high_wpm_sections)} typing section(s) require more than 80 WPM which is quite fast. See attached file for details.",
            attachment=("high_wpm_sections.txt", attachment_content)
        )
    
    return CheckResult(CheckStatus.PASS, "WPM")

