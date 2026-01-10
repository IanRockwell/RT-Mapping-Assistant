from .spread_check import check_spread_requirements
from .bg_check import check_background
from .tags_check import check_tags
from .preview_check import check_preview
from .gder_check import check_gder_tags
from .genre_check import check_genre
from .hs_inconsistency_check import check_hitsound_consistency

MAPSET_CHECKS = [
    check_spread_requirements,
    check_background,
    check_tags,
    check_preview,
    check_gder_tags,
    check_genre,
    check_hitsound_consistency,
]

