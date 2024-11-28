from typing import Callable

from diagnostipy.utils.scoring.confidence_functions import (
    entropy_based_confidence,
    rule_coverage_confidence,
    weighted_confidence,
)
from diagnostipy.utils.scoring.evaluation_functions import (
    binary_simple,
    default_evaluation,
)

CONFIDENCE_FUNCTIONS: dict[str, Callable] = {
    "weighted": weighted_confidence,
    "entropy": entropy_based_confidence,
    "rule_coverage": rule_coverage_confidence,
}

EVALUATION_FUNCTIONS: dict[str, Callable] = {
    "default": default_evaluation,
    "binary_simple": binary_simple,
}
