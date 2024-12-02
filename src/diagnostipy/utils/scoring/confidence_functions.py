import numpy as np

from diagnostipy.core.models.symptom_rule import SymptomRule


def _calculate_max_possible_weight(rules: list[SymptomRule]) -> float:
    """
    Calculate the maximum possible weight by prioritizing higher-weighted rules
    without overlap.

    Args:
        rules: List of all rules in the ruleset.

    Returns:
        Max possible weight as a float.
    """
    max_possible_weight = 0.0
    visited_conditions: set[str] = set()

    for rule in sorted(rules, key=lambda r: r.weight or 0, reverse=True):
        if rule.conditions and rule.conditions <= visited_conditions:
            continue

        max_possible_weight += rule.weight or 0

        if rule.conditions:
            visited_conditions.update(rule.conditions)

    return max_possible_weight


def _calculate_max_possible_rules(
    rules: list[SymptomRule],
) -> list[SymptomRule]:
    """
    Calculate the maximum number of non-overlapping rules.

    Args:
        rules: List of all rules in the ruleset.

    Returns:
        Maximum number of non-overlapping rules as an integer.
    """
    max_possible_rules = []
    visited_conditions: set[str] = set()

    for rule in sorted(rules, key=lambda r: r.weight or 0, reverse=True):
        if rule.conditions and rule.conditions <= visited_conditions:
            continue

        max_possible_rules.append(rule)

        if rule.conditions:
            visited_conditions.update(rule.conditions)

    return max_possible_rules


def weighted_confidence(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    *args,
    **kwargs,
) -> float:
    """
    Calculate confidence as a weighted average of rule weights.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.

    Returns:
        Confidence score as a float between 0 and 1.
    """
    if not applicable_rules:
        return 0.0

    total_weight = sum(rule.weight for rule in applicable_rules if rule.weight)
    max_possible_weight = _calculate_max_possible_weight(all_rules)

    if max_possible_weight == 0:
        return 0.0

    return min(total_weight / max_possible_weight, 1.0)


def entropy_based_confidence(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    *args,
    **kwargs,
) -> float:
    """
    Calculate confidence based on the entropy of rule weights.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.

    Returns:
        Confidence score as a float between 0 and 1.
    """
    if not applicable_rules:
        return 0.0

    weights = np.array([rule.weight for rule in applicable_rules if rule.weight])

    if weights.sum() == 0:
        return 0.0

    probabilities = weights / weights.sum()
    probabilities = np.clip(probabilities, 1e-9, 1.0)

    entropy = -np.sum(probabilities * np.log(probabilities))

    max_possible_rules = _calculate_max_possible_rules(all_rules)
    max_entropy = np.log(len(max_possible_rules)) if len(max_possible_rules) > 1 else 1

    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

    return min(normalized_entropy, 1.0)


def rule_coverage_confidence(
    applicable_rules: list[SymptomRule],
    all_rules: list[SymptomRule],
    *args,
    **kwargs,
) -> float:
    """
    Calculate confidence based on rule coverage.

    Args:
        applicable_rules: List of applicable rules.
        all_rules: List of all rules in the ruleset.

    Returns:
        Confidence score as a float between 0 and 1.
    """
    max_possible_rules = _calculate_max_possible_rules(all_rules)

    if max_possible_rules == 0:
        return 0.0

    return len(applicable_rules) / len(max_possible_rules)
