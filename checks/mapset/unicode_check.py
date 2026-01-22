from checks.base import CheckResult, CheckStatus


def has_unicode(text):
    if not text:
        return False
    return any(ord(char) > 127 for char in text)


def extract_unicode(text):
    if not text:
        return ""
    return "".join(char for char in text if ord(char) > 127)


def check_unicode_in_romanized(result):
    meta = result.get("meta", {})
    
    romanized_fields = {
        "artistName": meta.get("artistName", ""),
        "songName": meta.get("songName", ""),
    }
    
    issues = []
    unicode_suggestions = []
    
    for field_name, value in romanized_fields.items():
        if has_unicode(value):
            unicode_chars = extract_unicode(value)
            issues.append(f'"{field_name}" contains Unicode: "{value}"')
            unicode_suggestions.append(unicode_chars)
    
    if issues:
        unique_unicode = []
        for suggestion in unicode_suggestions:
            if suggestion not in unique_unicode:
                unique_unicode.append(suggestion)
        
        message = "\n".join(issues)
        
        return CheckResult(
            CheckStatus.FAIL,
            "Unicode",
            message
        )
    
    return CheckResult(CheckStatus.PASS, "Unicode")
