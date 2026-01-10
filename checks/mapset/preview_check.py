from checks.base import CheckResult, CheckStatus

def check_preview(result):
    meta = result.get("meta", {})
    preview_time = meta.get("previewTime", -1)
    
    if preview_time == -1:
        return CheckResult(
            CheckStatus.FAIL,
            "Preview",
            "Preview point not set."
        )
    
    return CheckResult(CheckStatus.PASS, "Preview")

