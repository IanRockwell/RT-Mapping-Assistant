from checks.base import CheckResult, CheckStatus

GENRES = [
    "rock",
    "pop",
    "electronic",
    "hip-hop",
    "jazz",
    "classical",
    "metal",
    "indie",
    "r&b",
    "bms",
    "country",
    "folk",
    "punk",
    "blues",
    "soul",
    "reggae",
    "edm",
    "house",
    "techno",
    "dubstep",
    "drum and bass",
    "dnb",
    "trance",
    "ambient",
    "lo-fi",
    "vocaloid",
    "j-pop",
    "j-rock",
    "k-pop",
    "anime",
    "video game",
    "soundtrack",
    "orchestral",
    "acoustic",
    "alternative",
    "experimental",
    "instrumental",
    "novelty",
]
def check_genre(result):
    meta = result.get("meta", {})
    tags = meta.get("tags", "").lower()
    tag_set = tags.split()

    matched = any(
        (genre in tags if " " in genre else genre in tag_set)
        for genre in GENRES
    )

    if matched:
        return CheckResult(CheckStatus.PASS, "Genre")

    return CheckResult(
        CheckStatus.WARNING,
        "Genre",
        "\n- No recognized genre tag found. Consider adding one of: " + ", ".join(GENRES[:10]) + ", etc."
    )

