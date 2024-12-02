from typing import Optional

import pytest

from diagnostipy.core.evaluator import Evaluator
from diagnostipy.core.models.diagnosis import DiagnosisBase
from diagnostipy.core.models.evaluation import BaseEvaluation


@pytest.fixture
def input_data():
    """
    Fixture providing a set of input data for evaluation.
    """
    return {"symptom1": 2, "symptom2": 0.3, "symptom3": True}


def test_evaluator_initialization(ruleset):
    evaluator = Evaluator(ruleset=ruleset)
    assert evaluator.ruleset == ruleset
    assert evaluator.data is None
    assert evaluator.diagnosis.total_score is None
    assert evaluator.diagnosis.label is None
    assert evaluator.diagnosis.confidence is None


def test_evaluator_evaluation_default_functions(ruleset, input_data):
    evaluator = Evaluator(ruleset=ruleset, data=input_data)
    evaluator.evaluate()

    assert evaluator.diagnosis.total_score
    assert evaluator.diagnosis.total_score > 0
    assert evaluator.diagnosis.label in ["High", "Medium", "Low"]
    assert evaluator.diagnosis.confidence
    assert 0.0 <= evaluator.diagnosis.confidence <= 1.0


def test_evaluator_run_method(ruleset, input_data):
    evaluator = Evaluator(ruleset=ruleset)
    results = evaluator.run(data=input_data)

    assert isinstance(results, DiagnosisBase)
    assert results.total_score
    assert results.total_score > 0
    assert results.label in ["High", "Medium", "Low"]
    assert results.confidence
    assert 0.0 <= results.confidence <= 1.0


def test_evaluator_with_custom_confidence_function(ruleset, input_data):
    def custom_confidence(applicable_rules, *args, **kwargs):
        return 1.0

    evaluator = Evaluator(ruleset=ruleset, confidence_function=custom_confidence)
    results = evaluator.run(data=input_data)

    assert isinstance(results, DiagnosisBase)
    assert results.total_score
    assert results.total_score > 0
    assert results.label in ["High", "Medium", "Low"]
    assert results.confidence
    assert results.confidence == 1.0


def test_evaluator_with_custom_evaluation_function(ruleset, input_data):
    class CustomEvaluation(BaseEvaluation):
        additional_field: str = "Custom"

    class CustomDiagnosis(DiagnosisBase):
        additional_field: Optional[str] = None
        total_score: float = 0.0
        label: Optional[str] = None
        confidence: Optional[float] = None

    def custom_evaluation(applicable_rules, *args, **kwargs):
        label = "Custom"
        score = 100.0
        return CustomEvaluation(label=label, score=score)

    evaluator = Evaluator(
        ruleset=ruleset,
        evaluation_function=custom_evaluation,
        diagnosis_model=CustomDiagnosis,
    )
    results = evaluator.run(data=input_data)

    assert isinstance(results, CustomDiagnosis)
    assert results.label == "Custom"
    assert results.total_score == 100.0
    assert results.additional_field == "Custom"


def test_evaluator_no_data_provided(ruleset):
    evaluator = Evaluator(ruleset=ruleset)

    with pytest.raises(ValueError, match="No data provided for evaluation."):
        evaluator.evaluate()


def test_evaluator_get_results_without_evaluation(ruleset, input_data):
    evaluator = Evaluator(ruleset=ruleset, data=input_data)

    with pytest.raises(ValueError, match="Evaluation has not been performed yet."):
        evaluator.get_results()


def test_evaluator_with_unknown_confidence_function(ruleset):
    """
    Test that a ValueError is raised when an unknown confidence function string \
    is provided.
    """
    unknown_function_name = "unknown_func"

    with pytest.raises(
        ValueError,
        match=f"Unknown confidence function '{unknown_function_name}'",
    ):
        Evaluator(ruleset=ruleset, confidence_function=unknown_function_name)


def test_evaluator_with_invalid_confidence_function_type(ruleset):
    """
    Test that an exception is raised when confidence_function is an invalid type.
    """
    invalid_confidence_function = 123  # Invalid type (not str or callable)

    with pytest.raises(TypeError, match="Invalid type for confidence_function"):
        Evaluator(
            ruleset=ruleset,
            confidence_function=invalid_confidence_function,  # type: ignore
        )


def test_invalid_evaluation_function(ruleset):
    with pytest.raises(ValueError, match="Unknown evaluation function 'invalid_func'"):
        Evaluator(ruleset, evaluation_function="invalid_func")


def test_invalid_evaluation_function_type(ruleset):
    with pytest.raises(TypeError, match="Invalid type for evaluation_function"):
        Evaluator(ruleset, evaluation_function=123)  # type: ignore
