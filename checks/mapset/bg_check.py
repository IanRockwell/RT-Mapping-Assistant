from checks.base import CheckResult, CheckStatus

def check_background(result):
    background = result.get("background")
    
    if not background:
        return CheckResult(CheckStatus.PASS, "BG")
    
    width = background.get("width", 0)
    height = background.get("height", 0)
    
    if width > 2560 or height > 1440:
        return CheckResult(
            CheckStatus.WARNING,
            "BG",
            f"\n- Background is larger than 2560x1440 ({width}x{height})."
        )
    
    return CheckResult(CheckStatus.PASS, "BG")
