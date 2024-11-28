from typing import Optional

import numpy as np

from diagnostipy.core.models.symptom_rule import SymptomRule


def weighted_confidence(
    applicable_rules: list[SymptomRule], *args, **kwargs
) -> float:
    """
    Calculate confidence as a weighted average of rule weights.

    Args:
        applicable_rules: List of applicable rules.

    Returns:
        Confidence score as a float between 0 and 1.
    """
    if not applicable_rules:
        return 0.0

    total_weight = sum(rule.weight for rule in applicable_rules if rule.weight)
    max_weight = max(rule.weight for rule in applicable_rules if rule.weight)
    return min(total_weight / (max_weight * len(applicable_rules)), 1.0)


def entropy_based_confidence(
    applicable_rules: list[SymptomRule], *args, **kwargs
) -> float:
    """
    Calculate confidence based on the entropy of rule weights.

    Args:
        applicable_rules: List of applicable rules.

    Returns:
        Confidence score as a float between 0 and 1.
    """
    if not applicable_rules:
        return 0.0

    weights = np.array(
        [rule.weight for rule in applicable_rules if rule.weight]
    )

    if weights.sum() == 0:
        return 0.0

    probabilities = weights / weights.sum()
    probabilities = np.clip(probabilities, 1e-9, 1.0)

    entropy = -np.sum(probabilities * np.log(probabilities))

    if len(applicable_rules) == 1:
        return 1.0

    max_entropy = np.log(len(applicable_rules))
    normalized_entropy = max(entropy / max_entropy, 0.0)
    return normalized_entropy


def rule_coverage_confidence(
    applicable_rules: list[SymptomRule],
    total_rules: Optional[int],
    *args,
    **kwargs
) -> float:
    """
    Calculate confidence based on rule coverage.

    Args:
        applicable_rules: List of applicable rules.
        total_rules: Total number of rules in the ruleset.

    Returns:
        Confidence score as a float between 0 and 1.
    """
    if total_rules is None or total_rules == 0:
        return 0.0

    return len(applicable_rules) / total_rules
