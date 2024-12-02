from diagnostipy.core.models.symptom_rule import SymptomRule


def test_symptom_rule_initialization():
    """
    Test that a SymptomRule initializes correctly with required attributes.
    """
    rule = SymptomRule(name="test_rule", weight=5.0, critical=True)

    assert rule.name == "test_rule"
    assert rule.weight == 5.0
    assert rule.critical is True
    assert rule.apply_condition is None


def test_symptom_rule_applies_without_condition():
    """
    Test that applies() returns False if no apply_condition is set.
    """
    rule = SymptomRule(name="test_rule", weight=5.0, critical=False)

    result = rule.applies(data={"key": "value"})

    assert result is False


def test_symptom_rule_applies_with_condition():
    """
    Test that applies() returns the correct result based on apply_condition.
    """
    rule = SymptomRule(
        name="test_rule",
        weight=3.5,
        critical=True,
        apply_condition=lambda data: data.get("key") == "value",
    )

    result = rule.applies(data={"key": "value"})
    assert result is True

    result = rule.applies(data={"key": "other_value"})
    assert result is False


def test_symptom_rule_applies_with_complex_condition():
    """
    Test a more complex apply_condition logic.
    """

    def complex_condition(data):
        return data.get("symptom1", 0) > 10 and data.get("symptom2", False)

    rule = SymptomRule(
        name="complex_rule",
        weight=4.5,
        critical=True,
        apply_condition=complex_condition,
    )

    result = rule.applies(data={"symptom1": 15, "symptom2": True})
    assert result is True

    result = rule.applies(data={"symptom1": 5, "symptom2": True})
    assert result is False

    result = rule.applies(data={"symptom1": 15, "symptom2": False})
    assert result is False


def test_symptom_rule_missing_fields():
    """
    Test SymptomRule with missing optional fields.
    """
    rule = SymptomRule(name="test_rule", weight=None)

    assert rule.weight is None
    assert rule.critical is False
    assert rule.apply_condition is None
    assert rule.applies(data={"key": "value"}) is False
