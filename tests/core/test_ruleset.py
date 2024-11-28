import pytest

from diagnostipy.core.models.symptom_rule import SymptomRule


def test_add_rule(ruleset):
    new_rule = SymptomRule(
        name="rule4",
        weight=2.0,
        critical=False,
        apply_condition=lambda data: True,
    )
    ruleset.add_rule(new_rule)

    assert len(ruleset.rules) == 4
    assert ruleset.get_rule("rule4") == new_rule

    with pytest.raises(ValueError):
        ruleset.add_rule(new_rule)


def test_get_rule(ruleset):
    rule = ruleset.get_rule("rule1")
    assert rule is not None
    assert rule.name == "rule1"

    non_existent_rule = ruleset.get_rule("non_existent_rule")
    assert non_existent_rule is None


def test_update_rule(ruleset):
    updated_rule = SymptomRule(
        name="rule1",
        weight=10.0,
        critical=True,
        apply_condition=lambda data: True,
    )
    result = ruleset.update_rule("rule1", updated_rule)

    assert result == updated_rule
    assert ruleset.get_rule("rule1").weight == 10.0

    non_existent_update = ruleset.update_rule("non_existent_rule", updated_rule)
    assert non_existent_update is None


def test_remove_rule(ruleset):
    result = ruleset.remove_rule("rule1")
    assert result is True
    assert ruleset.get_rule("rule1") is None
    assert len(ruleset.rules) == 2

    result = ruleset.remove_rule("non_existent_rule")
    assert result is False


def test_get_applicable_rules(ruleset):
    input_data = {"symptom1": 2, "symptom2": 0.5, "symptom3": True}
    applicable_rules = ruleset.get_applicable_rules(input_data)

    assert len(applicable_rules) == 3
    assert "rule1" in [rule.name for rule in applicable_rules]
    assert "rule2" in [rule.name for rule in applicable_rules]
    assert "rule3" in [rule.name for rule in applicable_rules]

    input_data = {"symptom1": 0, "symptom2": 2, "symptom3": False}
    applicable_rules = ruleset.get_applicable_rules(input_data)
    assert len(applicable_rules) == 0


def test_list_rules(ruleset):
    rule_names = ruleset.list_rules()
    assert len(rule_names) == 3
    assert "rule1" in rule_names
    assert "rule2" in rule_names
    assert "rule3" in rule_names
