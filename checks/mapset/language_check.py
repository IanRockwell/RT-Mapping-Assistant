from checks.base import CheckResult, CheckStatus

# List of recognized language tags
LANGUAGES = [
    "instrumental",
    "english",
    "japanese",
    "korean",
    "chinese",
    "spanish",
    "french",
    "german",
    "italian",
    "portuguese",
    "russian",

    # Languages not included on the site, but shouldn't be flagged if in tags anyways
    "conlang",
    "hindi",
    "arabic",
    "turkish",
    "vietnamese",
    "persian",
    "indonesian",
    "ukrainian",
    "romanian",
    "dutch",
    "thai",
    "greek",
    "somali",
    "malay",
    "hungarian",
    "czech",
    "norwegian",
    "finnish",
    "danish",
    "latvia",
    "lithuanian",
    "estonian",
    "punjabi",
    "bengali",
    "icelandic",
    "tagalog",
]


def check_language(result):
    """
    Check if at least one language tag exists in the tags field.
    """
    meta = result.get("meta", {})
    tags = meta.get("tags", "").lower()
    
    for language in LANGUAGES:
        if language in tags:
            return CheckResult(CheckStatus.PASS, "Language")
    
    return CheckResult(
        CheckStatus.WARNING,
        "Language",
        "No recognized language tag found. Consider adding one of: " + ", ".join(LANGUAGES[:10]) + ", etc."
    )
