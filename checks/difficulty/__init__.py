from .has_notes import check_has_notes
from .od_check import check_od

DIFFICULTY_CHECKS = [
    check_has_notes,
    check_od,
]

