import pytest

from diagnostipy.core.models.symptom_rule import SymptomRule
from diagnostipy.core.ruleset import SymptomRuleset


@pytest.fixture
def rules_with_conditions():
    """
    Fixture providing a set of rules with and without apply_condition.
    """
    return [
        SymptomRule(
            name="rule1",
            weight=5.0,
            critical=False,
            apply_condition=lambda data: data.get("symptom1", 0) > 1,
        ),
        SymptomRule(
            name="rule2",
            weight=3.5,
            critical=True,
            apply_condition=lambda data: data.get("symptom2", 0) < 1,
        ),
        SymptomRule(
            name="rule3",
            weight=1.5,
            critical=False,
            apply_condition=lambda data: data.get("symptom3"),
        ),
    ]


@pytest.fixture
def ruleset(rules_with_conditions):
    return SymptomRuleset(rules_with_conditions)
