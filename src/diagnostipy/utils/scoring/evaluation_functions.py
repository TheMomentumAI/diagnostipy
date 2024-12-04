from typing import Callable

from diagnostipy.core.models.evaluation import BaseEvaluation
from diagnostipy.core.models.symptom_rule import SymptomRule
from diagnostipy.utils.scoring.helpers import calculate_max_possible_weight


def binary_simple(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    *args,
    **kwargs,
) -> BaseEvaluation:
    """
    Binary evaluation logic to categorize based on total score compared to half of \
    total possible score.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.

    Returns:
        A binary evaluation result (High/Low).
    """
    total_score = sum(rule.weight or 0 for rule in applicable_rules)
    total_possible_score = calculate_max_possible_weight(all_rules)

    if total_score >= (total_possible_score / 2):
        return BaseEvaluation(label="High", score=total_score)
    else:
        return BaseEvaluation(label="Low", score=total_score)


def binary_scoring_based(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    score_function: Callable[[float], float],
    score_threshold: float = 0.5,
    *args,
    **kwargs,
) -> BaseEvaluation:
    """
    Scoring-based evaluation logic.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.
        score_function: Function to process the total score.
        threshold: Threshold for categorization.

    Returns:
        Evaluation result using the custom score function and threshold.
    """
    total_score = sum(rule.weight or 0 for rule in applicable_rules)
    processed_score = score_function(total_score)

    if processed_score >= score_threshold:
        return BaseEvaluation(label="High", score=processed_score)
    else:
        return BaseEvaluation(label="Low", score=processed_score)


def multiclass_simple(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    labels: list[str],
    *args,
    **kwargs,
) -> BaseEvaluation:
    """
    Multiclass evaluation logic based on total score and user-defined labels.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.
        labels: List of class labels in ascending order of severity.

    Returns:
        Evaluation result assigning a class based on score thresholds.
    """
    if len(labels) < 2:
        raise ValueError(
            "At least two labels must be provided for multiclass evaluation."
        )

    total_score = sum(rule.weight or 0 for rule in applicable_rules)
    total_possible_score = calculate_max_possible_weight(all_rules)

    if total_possible_score == 0:
        return BaseEvaluation(label=labels[0], score=total_score)

    step = total_possible_score / len(labels)

    for idx, threshold in enumerate(range(1, len(labels) + 1)):
        if total_score < step * threshold:
            return BaseEvaluation(label=labels[idx], score=total_score)

    return BaseEvaluation(label=labels[-1], score=total_score)


def multiclass_scoring_based(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    score_function: Callable[[float], float],
    threshold_label_map: dict[float, str],
    *args,
    **kwargs,
) -> BaseEvaluation:
    """
    Multiclass scoring-based evaluation logic.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.
        score_function: Function to process the total score.
        threshold_label_map: A dictionary mapping thresholds to labels. Thresholds
            should be provided in ascending order.

    Returns:
        Evaluation result assigning a class based on score thresholds.
    """
    if not threshold_label_map:
        raise ValueError("The `threshold_label_map` dictionary cannot be empty.")

    total_score = sum(rule.weight or 0 for rule in applicable_rules)
    processed_score = score_function(total_score)

    sorted_thresholds = sorted(threshold_label_map.items())

    for threshold, label in sorted_thresholds:
        if processed_score < threshold:
            return BaseEvaluation(label=label, score=processed_score)

    return BaseEvaluation(label=sorted_thresholds[-1][1], score=processed_score)
