import pytest

from diagnostipy.core.models.evaluation import BaseEvaluation
from diagnostipy.core.models.symptom_rule import SymptomRule
from diagnostipy.utils.scoring.evaluation_functions import (
    binary_simple,
    default_evaluation,
)


def test_default_evaluation_with_conditions(rules_with_conditions):
    input_data = {"symptom1": 2, "symptom2": 0.3, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    result = default_evaluation(applicable_rules)
    assert isinstance(result, BaseEvaluation)
    assert result.label == "High"
    assert result.score == pytest.approx(10.0)


def test_default_evaluation_no_applicable_rules(rules_with_conditions):
    input_data = {"symptom1": 0.5, "symptom2": 2, "symptom3": False}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    result = default_evaluation(applicable_rules)
    assert result.label == "Low"
    assert result.score == pytest.approx(0.0)


def test_default_evaluation_critical_rules():
    critical_rules = [
        SymptomRule(
            name="critical_rule",
            weight=1.0,
            critical=True,
            apply_condition=lambda data: True,
        )
    ]
    result = default_evaluation(critical_rules)
    assert result.label == "High"


def test_default_evaluation_with_conditions_medium(rules_with_conditions):
    input_data = {"symptom1": 2, "symptom2": 2, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    result = default_evaluation(applicable_rules)
    assert isinstance(result, BaseEvaluation)
    assert result.label == "Medium"
    assert result.score == pytest.approx(6.5)


def test_binary_simple_low_evaluation(rules_with_conditions):
    input_data = {"symptom1": 0.1, "symptom2": 0.1, "symptom3": False}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    all_rules = rules_with_conditions
    result = binary_simple(applicable_rules, all_rules)

    assert result.label == "Low"
    assert result.score < sum(rule.weight for rule in all_rules) / 2
