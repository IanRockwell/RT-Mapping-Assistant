from .notes_check import check_has_notes
from .od_check import check_od
from .keys_check import check_key_count
from .hold_check import check_hold_volume
from .wpm_check import check_typing_wpm
from .snap_check import check_unsnapped_notes
from .drain_coverage_check import check_drain_coverage
from .time_order_check import check_time_order
from .chord_alignment_check import check_chord_alignment

DIFFICULTY_CHECKS = [
    check_has_notes,
    check_time_order,
    check_chord_alignment,
    check_od,
    check_key_count,
    check_hold_volume,
    check_typing_wpm,
    check_unsnapped_notes,
    check_drain_coverage,
]

