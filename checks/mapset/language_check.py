from checks.base import CheckResult, CheckStatus


def check_language(result):
    """
    Ensure the map's set language appears in tags. If language is "Other", warn
    to put the correct language in tags.
    """
    meta = result.get("meta", {})
    language = (meta.get("language") or "").strip().lower()
    tags = (meta.get("tags") or "").lower()

    if language == "other":
        return CheckResult(
            CheckStatus.WARNING,
            "Language",
            "Language is set to \"Other\". Please ensure the correct language is in the tags.",
        )

    if not language:
        return CheckResult(CheckStatus.PASS, "Language")

    if language not in tags:
        return CheckResult(
            CheckStatus.FAIL,
            "Language",
            f"The map language is \"{language}\" but no matching language tag was found in the tags. Add the language to the tags.",
        )

    return CheckResult(CheckStatus.PASS, "Language")
