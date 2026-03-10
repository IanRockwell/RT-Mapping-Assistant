from checks.base import CheckResult, CheckStatus


def check_language(result):
    meta = result.get("meta", {})
    language = (meta.get("language") or "").strip().lower()
    tag_set = set((meta.get("tags") or "").lower().split())

    if language == "other":
        return CheckResult(
            CheckStatus.WARNING,
            "Language",
            "\n- Language is set to \"Other\". Please ensure the correct language is in the tags.",
        )

    if language not in tag_set:
        return CheckResult(
            CheckStatus.FAIL,
            "Language",
            f"\n- The map language is \"{language}\" but no matching language tag was found in the tags. Add the language to the tags.",
        )

    return CheckResult(CheckStatus.PASS, "Language")
