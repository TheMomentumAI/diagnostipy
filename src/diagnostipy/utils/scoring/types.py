from typing import Protocol

from diagnostipy.core.models.evaluation import BaseEvaluation
from diagnostipy.core.models.symptom_rule import SymptomRule


class ConfidenceFunction(Protocol):
    def __call__(
        self, applicable_rules: list[SymptomRule], *args, **kwargs
    ) -> float:
        ...


class EvaluationFunction(Protocol):
    def __call__(
        self,
        applicable_rules: list[SymptomRule],
        all_rules: list[SymptomRule],
        *args,
        **kwargs
    ) -> BaseEvaluation:
        ...
