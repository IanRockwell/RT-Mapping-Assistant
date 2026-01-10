from .notes_check import check_has_notes
from .od_check import check_od
from .keys_check import check_key_count
from .hold_check import check_hold_volume
from .wpm_check import check_typing_wpm

DIFFICULTY_CHECKS = [
    check_has_notes,
    check_od,
    check_key_count,
    #check_hold_volume,
    check_typing_wpm,
]

