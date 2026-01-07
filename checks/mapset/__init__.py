from .spread_requirements import check_spread_requirements
from .background_check import check_background
from .tags_check import check_tags
from .preview_check import check_preview

MAPSET_CHECKS = [
    check_spread_requirements,
    check_background,
    check_tags,
    check_preview,
]

