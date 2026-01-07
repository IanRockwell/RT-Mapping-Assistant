from .base import CheckResult, CheckStatus
from .mapset import MAPSET_CHECKS
from .difficulty import DIFFICULTY_CHECKS


def run_meta_checks(result):
    return [check(result) for check in MAPSET_CHECKS]


def run_difficulty_checks(difficulty):
    return [check(difficulty) for check in DIFFICULTY_CHECKS]
