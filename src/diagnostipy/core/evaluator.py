from typing import Any, Callable, Optional

from diagnostipy.core.models.diagnosis import Diagnosis, DiagnosisBase
from diagnostipy.core.ruleset import SymptomRuleset
from diagnostipy.core.typing import FunctionMap, T
from diagnostipy.utils.enums import ConfidenceFunctionEnum, EvaluationFunctionEnum
from diagnostipy.utils.scoring import CONFIDENCE_FUNCTIONS, EVALUATION_FUNCTIONS
from diagnostipy.utils.scoring.types import ConfidenceFunction, EvaluationFunction


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
            Optional[EvaluationFunction] | EvaluationFunctionEnum
        ) = EvaluationFunctionEnum.BINARY_SIMPLE,
        confidence_function: (
            Optional[ConfidenceFunction] | ConfidenceFunctionEnum
        ) = ConfidenceFunctionEnum.WEIGHTED,
        diagnosis_model: type[DiagnosisBase] = Diagnosis,
    ):
        self.data = data
        self.ruleset = ruleset
        self.diagnosis_model = diagnosis_model
        self.diagnosis = self.diagnosis_model()
        self._evaluation_function = self._resolve_function(
            evaluation_function,
            EvaluationFunctionEnum,
            EVALUATION_FUNCTIONS,
            "evaluation_function",
        )
        self._confidence_function = self._resolve_function(
            confidence_function,
            ConfidenceFunctionEnum,
            CONFIDENCE_FUNCTIONS,
            "confidence_function",
        )

    def _resolve_function(
        self,
        func_input: Optional[Callable[..., Any] | T | str],
        enum_type: type[T],
        func_map: FunctionMap[T],
        func_name: str,
    ) -> Callable[..., Any]:
        """
        Resolves and validates a function input.

        Args:
            func_input: The input, which can be an enum, string, or callable.
            enum_type: The enum class for validation.
            func_map: A dictionary mapping enums to functions.
            func_name: The name of the function type (for error messages).

        Returns:
            The resolved callable function.

        Raises:
            ValueError: If the function cannot be resolved.
            TypeError: If the input type is invalid.
        """
        if isinstance(func_input, enum_type):
            return self._get_function_from_enum(
                func_input, func_map, enum_type, func_name
            )

        if isinstance(func_input, str):
            return self._get_function_from_str(
                func_input, func_map, enum_type, func_name
            )

        if callable(func_input):
            return func_input

        raise TypeError(f"Invalid type for {func_name}: {type(func_input)}. ")

    def _get_function_from_enum(
        self,
        enum_value: T,
        func_map: dict[T, Callable[..., Any]],
        enum_type: type[T],
        func_name: str,
    ) -> Callable[..., Any]:
        func = func_map.get(enum_value)
        if not func:
            raise ValueError(
                f"Unknown {func_name} '{enum_value}'. "
                f"Available options are: {[e.value for e in enum_type]}"
            )
        return func

    def _get_function_from_str(
        self,
        str_value: str,
        func_map: dict[T, Callable[..., Any]],
        enum_type: type[T],
        func_name: str,
    ) -> Callable[..., Any]:
        try:
            enum_value = enum_type(str_value)
            return self._get_function_from_enum(
                enum_value, func_map, enum_type, func_name
            )
        except ValueError:
            raise ValueError(
                f"Unknown {func_name} '{str_value}'. "
                f"Available options are: {[e.value for e in enum_type]}"
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
                applicable_rules, self.ruleset.rules, *args, **kwargs
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
            data (Optional[Any]): Input data for evaluation. If provided, this updates \
            the current data.

        Returns:
            DiagnosisBase: Evaluation results containing risk level, confidence, and \
            total score.
        """
        if data is not None:
            self.data = data

        self.evaluate(*args, **kwargs)
        return self.get_results()
