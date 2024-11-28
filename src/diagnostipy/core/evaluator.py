from typing import Any, Callable, Optional

from diagnostipy.core.models.diagnosis import Diagnosis, DiagnosisBase
from diagnostipy.core.models.symptom_rule import SymptomRule
from diagnostipy.core.ruleset import SymptomRuleset
from diagnostipy.utils.scoring import CONFIDENCE_FUNCTIONS, EVALUATION_FUNCTIONS
from diagnostipy.utils.scoring.evaluation_functions import default_evaluation
from diagnostipy.utils.scoring.types import (
    ConfidenceFunction,
    EvaluationFunction,
)


class Evaluator:
    """
    Generalized evaluator class for assessing risk or scoring based on rules.

    Attributes:
        data (Any): Input data for evaluation.
        ruleset (SymptomRuleset): A set of rules used for evaluation.
        total_score (float): Total score based on applicable rules.
        confidence (Optional[float]): Confidence level of the evaluation.
        risk_level (Optional[str]): Risk level determined by the evaluation.
    """

    def __init__(
        self,
        ruleset: SymptomRuleset,
        data: Optional[Any] = None,
        evaluation_function: (
            Optional[EvaluationFunction] | str
        ) = "binary_simple",
        confidence_function: Optional[ConfidenceFunction] | str = "weighted",
        diagnosis_model: type[DiagnosisBase] = Diagnosis,
    ):
        self.data = data
        self.ruleset = ruleset
        self.diagnosis_model = diagnosis_model
        self.diagnosis = self.diagnosis_model()
        self._evaluation_function = evaluation_function or default_evaluation

        if isinstance(evaluation_function, str):
            self._evaluation_function = EVALUATION_FUNCTIONS.get(
                evaluation_function
            )
            if self._evaluation_function is None:
                raise ValueError(
                    f"Unknown evaluation function '{evaluation_function}'. "
                    f"Available options are: {list(EVALUATION_FUNCTIONS.keys())}"
                )
        elif callable(evaluation_function):
            self._evaluation_function = evaluation_function
        else:
            raise TypeError(
                f"Invalid type for evaluation_function: {type(evaluation_function)}. "
                "Expected str or callable."
            )

        if isinstance(confidence_function, str):
            self._confidence_function = CONFIDENCE_FUNCTIONS.get(
                confidence_function
            )
            if self._confidence_function is None:
                raise ValueError(
                    f"Unknown confidence function '{confidence_function}'. "
                    f"Available options are: {list(CONFIDENCE_FUNCTIONS.keys())}"
                )
        elif callable(confidence_function):
            self._confidence_function = confidence_function
        else:
            raise TypeError(
                f"Invalid type for confidence_function: {type(confidence_function)}. "
                "Expected str or callable."
            )

    def evaluate(self, *args, **kwargs) -> None:
        """
        Perform evaluation based on the ruleset and the input data.

        Args:
            *args: Positional arguments to pass to evaluation and confidence functions.
            **kwargs: Keyword arguments to pass to evaluation and confidence functions.
        """
        if self.data is None:
            raise ValueError("No data provided for evaluation.")

        applicable_rules = self.ruleset.get_applicable_rules(self.data)

        self.evaluation_result = self._evaluation_function(
            applicable_rules,
            self.ruleset.rules,
            *args,
            **kwargs,
        )

        self.diagnosis = self.diagnosis_model(
            label=self.evaluation_result.label,
            total_score=self.evaluation_result.score,
            confidence=self._confidence_function(
                applicable_rules, *args, **kwargs
            ),
            **self.evaluation_result.model_dump(exclude={"label", "score"}),
        )

    def get_results(self) -> DiagnosisBase:
        """
        Retrieve the evaluation results.

        Returns:
            A dictionary containing risk level, confidence, and total score.
        """
        if self.diagnosis.label is None or self.diagnosis.confidence is None:
            raise ValueError("Evaluation has not been performed yet.")

        return self.diagnosis

    def run(self, data: Optional[Any] = None, *args, **kwargs) -> DiagnosisBase:
        """
        Perform evaluation and return results in a single method.

        Args:
            data (Optional[Any]): Input data for evaluation. If provided, this updates the current data.

        Returns:
            DiagnosisBase: Evaluation results containing risk level, confidence, and total score.
        """
        if data is not None:
            self.data = data

        self.evaluate(*args, **kwargs)
        return self.get_results()
