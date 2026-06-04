from .spread_check import check_spread_requirements
from .bg_check import check_background
from .tags_check import check_tags
from .preview_check import check_preview
from .gder_check import check_gder_tags
from .genre_check import check_genre
from .language_check import check_language
from .hs_inconsistency_check import check_hitsound_consistency
from .unicode_check import check_unicode_in_romanized
from .audio_check import check_audio_quality

MAPSET_CHECKS = [
    check_spread_requirements,
    check_background,
    check_tags,
    check_preview,
    check_gder_tags,
    check_genre,
    check_language,
    check_hitsound_consistency,
    check_unicode_in_romanized,
    check_audio_quality,
]

