from checks.base import CheckResult, CheckStatus


def check_audio_quality(result):
    audio = result.get("audio")
    if not audio:
        return CheckResult(CheckStatus.PASS, "Audio Quality")

    avg_br = audio.get("average_bitrate")
    file_br = audio.get("bitrate")

    if avg_br is None or file_br is None:
        return CheckResult(CheckStatus.PASS, "Audio Quality")

    if file_br - avg_br >= 64:
        return CheckResult(
            CheckStatus.WARNING,
            "Audio Quality",
            f"Audio may be overencoded. Spectral quality suggests ~{avg_br:.0f} kbps but file reports {file_br:.0f} kbps."
        )

    return CheckResult(CheckStatus.PASS, "Audio Quality")
