from checks.base import CheckResult, CheckStatus

# List of recognized genre tags
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
]


def check_genre(result):
    """
    Check if at least one genre tag exists in the tags field.
    """
    meta = result.get("meta", {})
    tags = meta.get("tags", "").lower()
    
    for genre in GENRES:
        if genre in tags:
            return CheckResult(CheckStatus.PASS, "Genre Check")
    
    return CheckResult(
        CheckStatus.WARNING,
        "Missing Genre Tag",
        "No recognized genre tag found. Consider adding one of: " + ", ".join(GENRES[:10]) + ", etc."
    )

