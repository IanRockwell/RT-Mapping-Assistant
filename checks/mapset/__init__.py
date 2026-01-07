from .spread_requirements import check_spread_requirements
from .background_check import check_background

MAPSET_CHECKS = [
    check_spread_requirements,
    check_background,
]

