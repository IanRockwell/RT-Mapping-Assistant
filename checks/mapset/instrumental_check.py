from checks.base import CheckResult, CheckStatus


def check_instrumental_default(result):
    """
    Warn when language is "instrumental" (the default), so the mapper confirms
    the song is actually an instrumental.
    """
    meta = result.get("meta", {})
    language = (meta.get("language") or "").strip().lower()
    if language == "instrumental":
        return CheckResult(
            CheckStatus.WARNING,
            "Instrumental (default language)",
            "Language is set to the default \"instrumental\". Ignore if this song is actually an instrumental.",
        )
    return CheckResult(CheckStatus.PASS, "Instrumental (default language)")
