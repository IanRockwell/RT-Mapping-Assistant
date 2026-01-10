from checks.base import CheckResult, CheckStatus

def check_background(result):
    background = result.get("background")
    
    if not background:
        return CheckResult(CheckStatus.PASS, "Background Check")
    
    width = background.get("width", 0)
    height = background.get("height", 0)
    
    warnings = []
    
    if width > 2560 or height > 1440:
        warnings.append(f"Background is larger than 2560x1440 ({width}x{height}).")
    
    if width * 9 != height * 16:
        warnings.append("Background is not 16:9.")
    
    if warnings:
        return CheckResult(
            CheckStatus.WARNING,
            "Background Check",
            " ".join(warnings)
        )
    
    return CheckResult(CheckStatus.PASS, "Background Check")

