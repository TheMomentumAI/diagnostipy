from typing import Any, Callable, Optional

from pydantic import BaseModel


class SymptomRule(BaseModel):
    """
    Represents a rule for evaluating symptoms.

    Attributes:
        name (str): Unique identifier for the rule.
        weight (float): Impact of the rule on the risk score.
        conditions (Optional[Set[str]]): Set of fields (symptoms) required for the \
        rule to be evaluated.
        critical (bool): Whether the rule is critical (e.g., high-priority).
        apply_condition (Optional[Callable[[dict[str, Any]], bool]]):
            Custom function to determine if the rule applies.
    """

    name: str
    weight: Optional[float]
    critical: bool = False
    apply_condition: Optional[Callable[..., bool]] = None
    conditions: Optional[set[str]] = None

    def _get_field_value(self, data: Any, field: str) -> Optional[Any]:
        """
        Generalized method to retrieve a field's value from different types of data.

        Args:
            data: The input data, which can be of any type.
            field: The name of the field to retrieve.

        Returns:
            The value of the field if it exists, otherwise None.
        """
        if isinstance(data, dict):
            return data.get(field, None)

        if hasattr(data, field):
            return getattr(data, field, None)

        return None

    def applies(self, data: Any) -> bool:
        """
        Check if the rule applies to the provided data.

        Args:
            data: Input data to evaluate. Can be of any type.

        Returns:
            bool: True if the rule applies, otherwise False.
        """
        if self.apply_condition:
            return self.apply_condition(data)

        if not self.conditions:
            return True

        for condition in self.conditions:
            value = self._get_field_value(data, condition)
            if not value:
                return False

        return True
