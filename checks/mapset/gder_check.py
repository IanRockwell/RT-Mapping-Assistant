import re
from checks.base import CheckResult, CheckStatus


def check_gder_tags(result):
    meta = result.get("meta", {})
    tags = meta.get("tags", "").lower().split()
    difficulties = result.get("difficulties", [])
    
    missing_gders = []
    
    for diff in difficulties:
        diff_name = diff.get("data", {}).get("name", "")
        
        # Match word followed by 's or word ending in s followed by '
        # Pattern 1: word's (e.g., "ZABRID'S") -> check "zabrid"
        # Pattern 2: words' (e.g., "JAMES'") -> check "james"
        matches_apostrophe_s = re.findall(r"(\w+)'s\b", diff_name, re.IGNORECASE)
        matches_s_apostrophe = re.findall(r"(\w+s)'\b", diff_name, re.IGNORECASE)
        
        for match in matches_apostrophe_s:
            name_to_check = match.lower()
            if name_to_check not in tags:
                missing_gders.append((diff_name, name_to_check))
        
        for match in matches_s_apostrophe:
            # For s' pattern, the captured group includes the 's'
            name_to_check = match.lower()
            if name_to_check not in tags:
                missing_gders.append((diff_name, name_to_check))
    
    if missing_gders:
        messages = []
        for diff_name, gder_name in missing_gders:
            messages.append(f'"{diff_name}" is possessive but "{gder_name}" isn\'t in the tags, ignore if not a user.')
        
        return CheckResult(
            CheckStatus.WARNING,
            "Missing GDers in tags.",
            "\n".join(messages)
        )
    
    return CheckResult(CheckStatus.PASS, "GDer Tags Check")

