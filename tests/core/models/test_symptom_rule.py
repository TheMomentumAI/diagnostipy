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
    assert rule.applies(data={"key": "value"}) is True


def test_symptom_rule_get_field_value_from_object():
    """
    Test _get_field_value retrieves a value from an object with attributes.
    """

    class MockData:
        symptom1 = 10
        symptom2 = True

    rule = SymptomRule(name="test_rule", weight=5.0)

    value = rule._get_field_value(MockData(), "symptom1")
    assert value == 10

    value = rule._get_field_value(MockData(), "symptom3")
    assert value is None


def test_symptom_rule_get_field_value_invalid_type():
    """
    Test _get_field_value with unsupported data type.
    """
    rule = SymptomRule(name="test_rule", weight=5.0)

    value = rule._get_field_value(123, "symptom1")
    assert value is None


def test_symptom_rule_applies_with_conditions():
    """
    Test applies() logic when conditions are provided.
    """
    rule = SymptomRule(name="test_rule", weight=5.0, conditions={"field1", "field2"})

    data = {"field1": True, "field2": True}
    assert rule.applies(data) is True

    data = {"field1": True, "field2": False}
    assert rule.applies(data) is False

    data = {"field1": False, "field2": False}
    assert rule.applies(data) is False

    data = {}
    assert rule.applies(data) is False


def test_symptom_rule_applies_with_empty_conditions():
    """
    Test applies() logic when conditions are an empty set.
    """
    rule = SymptomRule(name="test_rule", weight=5.0, conditions=set())

    data = {"field1": True, "field2": False}
    assert rule.applies(data) is True


def test_symptom_rule_applies_no_conditions_or_apply_condition():
    """
    Test applies() logic when neither conditions nor apply_condition is set.
    """
    rule = SymptomRule(name="test_rule", weight=5.0)

    data = {"field1": True}
    assert rule.applies(data) is True
