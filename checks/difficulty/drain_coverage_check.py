import logging

from checks.base import CheckResult, CheckStatus
from apis.rhythmtyper import calculate_drain_time, format_length

logger = logging.getLogger(__name__)


def check_drain_coverage(difficulty, meta=None):
    audio_duration = meta.get("_audio_duration") if meta else None
    drain_ms = calculate_drain_time(difficulty)
    drain_seconds = drain_ms / 1000
    ratio = drain_seconds / audio_duration

    if ratio < 0.6:
        return CheckResult(
            CheckStatus.FAIL,
            "Drain Coverage",
            f"\n- Drain time ({format_length(drain_seconds)}) is {ratio * 100:.1f}% of audio ({format_length(audio_duration)}). Must map at least 60% of the audio.",
        )

    return CheckResult(CheckStatus.PASS, "Drain Coverage")
