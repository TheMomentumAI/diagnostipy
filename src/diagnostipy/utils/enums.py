from enum import Enum


class EvaluationFunctionEnum(str, Enum):
    BINARY_SIMPLE = "binary_simple"


class ConfidenceFunctionEnum(str, Enum):
    WEIGHTED = "weighted"
    ENTROPY = "entropy"
    RULE_COVERAGE = "rule_coverage"
