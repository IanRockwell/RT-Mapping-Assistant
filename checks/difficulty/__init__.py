from .has_notes import check_has_notes
from .od_check import check_od
from .key_count import check_key_count
from .hold_volume import check_hold_volume

DIFFICULTY_CHECKS = [
    check_has_notes,
    check_od,
    check_key_count,
    check_hold_volume,
]

