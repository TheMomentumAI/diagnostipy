from diagnostipy.utils.enums import ConfidenceFunctionEnum, EvaluationFunctionEnum
from diagnostipy.utils.scoring.confidence_functions import (
    entropy_based_confidence,
    rule_coverage_confidence,
    weighted_confidence,
)
from diagnostipy.utils.scoring.evaluation_functions import (
    binary_scoring_based,
    binary_simple,
    multiclass_scoring_based,
    multiclass_simple,
)
from diagnostipy.utils.scoring.types import ConfidenceFunction, EvaluationFunction

CONFIDENCE_FUNCTIONS: dict[ConfidenceFunctionEnum, ConfidenceFunction] = {
    ConfidenceFunctionEnum.WEIGHTED: weighted_confidence,
    ConfidenceFunctionEnum.ENTROPY: entropy_based_confidence,
    ConfidenceFunctionEnum.RULE_COVERAGE: rule_coverage_confidence,
}

EVALUATION_FUNCTIONS: dict[EvaluationFunctionEnum, EvaluationFunction] = {
    EvaluationFunctionEnum.BINARY_SIMPLE: binary_simple,
    EvaluationFunctionEnum.BINARY_SCORING_BASED: binary_scoring_based,
    EvaluationFunctionEnum.MULTICLASS_SIMPLE: multiclass_simple,
    EvaluationFunctionEnum.MULTICLASS_SCORING_BASED: multiclass_scoring_based,
}
