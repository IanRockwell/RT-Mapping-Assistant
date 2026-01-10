from checks.base import CheckResult, CheckStatus

def check_tags(result):
    meta = result.get("meta", {})
    tags = meta.get("tags", "")
    
    if not tags or not tags.strip():
        return CheckResult(
            CheckStatus.WARNING,
            "Tags",
            "Tags field is empty."
        )
    
    return CheckResult(CheckStatus.PASS, "Tags")

