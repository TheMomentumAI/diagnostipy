from math import tanh

import pytest

from diagnostipy.core.models.evaluation import BaseEvaluation
from diagnostipy.utils.scoring.evaluation_functions import (
    binary_scoring_based,
    binary_simple,
    multiclass_scoring_based,
    multiclass_simple,
)


def test_binary_simple_low_evaluation(rules_with_conditions):
    input_data = {"symptom1": 0.1, "symptom2": 0.1, "symptom3": False}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    result = binary_simple(applicable_rules, rules_with_conditions)

    assert result.label == "Low"
    assert result.score < sum(rule.weight for rule in rules_with_conditions) / 2


def test_binary_scoring_based_high_score(rules_with_conditions):
    input_data = {"symptom1": 2, "symptom2": 2, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    all_rules = rules_with_conditions
    result = binary_scoring_based(
        applicable_rules, all_rules, score_function=tanh, score_threshold=0.5
    )

    assert isinstance(result, BaseEvaluation)
    assert result.label == "High"
    assert result.score >= 0.5


def test_binary_scoring_based_low_score(rules_with_conditions):
    input_data = {"symptom1": 0.1, "symptom2": 0.1, "symptom3": False}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    all_rules = rules_with_conditions
    result = binary_scoring_based(
        applicable_rules,
        all_rules,
        score_function=lambda x: 1 / x,
        score_threshold=0.3,
    )

    assert result.label == "Low"
    assert result.score < 0.3


def test_multiclass_simple_low_label(rules_with_conditions):
    input_data = {"symptom1": 0.1, "symptom2": 1.2, "symptom3": False}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    labels = ["Low", "Medium", "High"]
    all_rules = rules_with_conditions
    result = multiclass_simple(applicable_rules, all_rules, labels)

    assert isinstance(result, BaseEvaluation)
    assert result.label == "Low"


def test_multiclass_simple_high_label(rules_with_conditions):
    input_data = {"symptom1": 2, "symptom2": 0.5, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    labels = ["Low", "Medium", "High"]
    all_rules = rules_with_conditions
    result = multiclass_simple(applicable_rules, all_rules, labels)

    assert result.label == "High"


def test_multiclass_scoring_based_low_label(rules_with_conditions):
    input_data = {"symptom1": 0.1, "symptom2": 0.1, "symptom3": False}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    all_rules = rules_with_conditions
    threshold_label_map = {
        0.3: "Low",
        0.6: "Medium",
        0.9: "High",
    }

    result = multiclass_scoring_based(
        applicable_rules,
        all_rules,
        score_function=lambda x: 1 / x,
        threshold_label_map=threshold_label_map,
    )

    assert isinstance(result, BaseEvaluation)
    assert result.label == "Low"


def test_multiclass_scoring_based_high_label(rules_with_conditions):
    input_data = {"symptom1": 2, "symptom2": 2, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    all_rules = rules_with_conditions
    threshold_label_map = {
        0.3: "Low",
        0.6: "Medium",
        0.9: "High",
    }

    result = multiclass_scoring_based(
        applicable_rules,
        all_rules,
        score_function=tanh,
        threshold_label_map=threshold_label_map,
    )

    assert result.label == "High"


def test_multiclass_scoring_based_empty_threshold_label_map(
    rules_with_conditions,
):
    input_data = {"symptom1": 2, "symptom2": 2, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]
    all_rules = rules_with_conditions

    with pytest.raises(
        ValueError,
        match="The `threshold_label_map` dictionary cannot be empty.",
    ):
        multiclass_scoring_based(
            applicable_rules,
            all_rules,
            score_function=tanh,
            threshold_label_map={},
        )


def test_multiclass_simple_last_label(rules_with_conditions):
    input_data = {"symptom1": 3, "symptom2": 0.1, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    labels = ["Low", "Medium", "High"]
    all_rules = rules_with_conditions
    result = multiclass_simple(applicable_rules, all_rules, labels)

    assert result.label == "High"
    assert result.score >= sum(rule.weight or 0 for rule in rules_with_conditions)


def test_multiclass_scoring_based_last_label(rules_with_conditions):
    input_data = {"symptom1": 3, "symptom2": 2, "symptom3": True}
    applicable_rules = [
        rule for rule in rules_with_conditions if rule.applies(input_data)
    ]

    all_rules = rules_with_conditions
    threshold_label_map = {
        0.3: "Low",
        0.6: "Medium",
        0.9: "High",
    }

    result = multiclass_scoring_based(
        applicable_rules,
        all_rules,
        score_function=lambda x: x,
        threshold_label_map=threshold_label_map,
    )

    assert result.label == "High"
    assert result.score >= max(threshold_label_map.keys())
