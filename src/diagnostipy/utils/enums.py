from enum import Enum


class EvaluationFunctionEnum(str, Enum):
    BINARY_SIMPLE = "binary_simple"
    BINARY_SCORING_BASED = "binary_scoring_based"
    MULTICLASS_SIMPLE = "multiclass_simple"
    MULTICLASS_SCORING_BASED = "multiclass_scoring_based"


class ConfidenceFunctionEnum(str, Enum):
    WEIGHTED = "weighted"
    ENTROPY = "entropy"
    RULE_COVERAGE = "rule_coverage"
