from typing import Any, Callable, Optional

from pydantic import BaseModel


class SymptomRule(BaseModel):
    """
    Represents a rule for evaluating symptoms.

    Attributes:
        name (str): Unique identifier for the rule.
        weight (float): Impact of the rule on the risk score.
        conditions (Optional[List[str]]): Fields required for the rule to be evaluated.
        critical (bool): Whether the rule is critical (e.g., high-priority).
        apply_condition (Optional[Callable[[dict[str, Any]], bool]]):
            Custom function to determine if the rule applies.
    """

    name: str
    weight: Optional[float]
    critical: bool = False
    apply_condition: Optional[Callable[..., bool]] = None

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

        return False
