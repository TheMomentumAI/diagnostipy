from typing import Any, Optional

from diagnostipy.core.models.symptom_rule import SymptomRule


class SymptomRuleset:
    def __init__(self, rules: Optional[list[SymptomRule]] = None):
        """
        A collection of rules for evaluating symptoms.

        Args:
            rules: List of rules to apply.
        """
        self.rules: list[SymptomRule] = rules or []

    def add_rule(self, rule: SymptomRule) -> SymptomRule:
        """
        Add a new rule to the ruleset.

        Args:
            rule: The SymptomRule object to add.

        Returns:
            The added SymptomRule object.
        """
        if self.get_rule(rule.name):
            raise ValueError(
                f"A rule with the name '{rule.name}' already exists."
            )
        self.rules.append(rule)
        return rule

    def get_rule(self, name: str) -> Optional[SymptomRule]:
        """
        Retrieve a rule by its name.

        Args:
            name: The name of the rule to retrieve.

        Returns:
            The matching SymptomRule object if found, otherwise None.
        """
        return next((rule for rule in self.rules if rule.name == name), None)

    def update_rule(
        self,
        name: str,
        updated_rule: SymptomRule,
    ) -> Optional[SymptomRule]:
        """
        Update an existing rule.

        Args:
            name: The name of the rule to update.
            updated_rule: The new SymptomRule object to replace the existing rule.

        Returns:
            The updated SymptomRule object, or None if not found.
        """
        existing_rule = self.get_rule(name)
        if not existing_rule:
            return None

        self.rules = [rule for rule in self.rules if rule.name != name]
        self.rules.append(updated_rule)
        return updated_rule

    def remove_rule(self, name: str) -> bool:
        """
        Remove a rule by its name.

        Args:
            name: The name of the rule to remove.

        Returns:
            True if the rule was successfully removed, False if not found.
        """
        rule = self.get_rule(name)
        if rule:
            self.rules.remove(rule)
            return True
        return False

    def get_applicable_rules(self, data: Any) -> list[SymptomRule]:
        """
        Return all rules that apply to the provided data.

        Args:
            data: Input data to evaluate. Can be of any type.

        Returns:
            A list of applicable rules.
        """
        return [rule for rule in self.rules if rule.applies(data)]

    def list_rules(self) -> list[str]:
        """
        List the names of all rules in the ruleset.

        Returns:
            A list of rule names.
        """
        return [rule.name for rule in self.rules]
