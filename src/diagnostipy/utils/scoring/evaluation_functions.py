from diagnostipy.core.models.evaluation import BaseEvaluation
from diagnostipy.core.models.symptom_rule import SymptomRule


# TODO function used in other project, may be too specific and removed
def default_evaluation(
    applicable_rules: list[SymptomRule], *args, **kwargs
) -> BaseEvaluation:
    """
    Default evaluation logic to categorize based on total score.

    Args:
        total_score: The total score calculated from applicable rules.
        applicable_rules: List of applicable rules.

    Returns:
        A default evaluation result (categorical).
    """
    critical_rules_applied = any(rule.critical for rule in applicable_rules)
    total_score = sum(rule.weight or 0 for rule in applicable_rules)

    if total_score >= 10.0 or critical_rules_applied:
        return BaseEvaluation(label="High", score=total_score)
    elif total_score >= 5.0:
        return BaseEvaluation(label="Medium", score=total_score)
    else:
        return BaseEvaluation(label="Low", score=total_score)


def binary_simple(
    applicable_rules: list[SymptomRule], all_rules: list[SymptomRule], *args, **kwargs
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
    total_possible_score = sum(rule.weight or 0 for rule in all_rules)

    if total_score >= (total_possible_score / 2):
        return BaseEvaluation(label="High", score=total_score)
    else:
        return BaseEvaluation(label="Low", score=total_score)
