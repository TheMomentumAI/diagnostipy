from diagnostipy.core.models.symptom_rule import SymptomRule


def calculate_max_possible_weight(rules: list[SymptomRule]) -> float:
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


def calculate_max_possible_rules(
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
