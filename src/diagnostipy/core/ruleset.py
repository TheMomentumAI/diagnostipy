from typing import Any, Optional

from diagnostipy.core.models.symptom_rule import SymptomRule


class SymptomRuleset:
    def __init__(
        self,
        rules: Optional[list[SymptomRule]] = None,
        exclude_overlaps: bool = True,
    ):
        """
        A collection of rules for evaluating symptoms.

        Args:
            rules: List of rules to apply.
            exclude_overlaps: Whether to exclude overlapping rules by default.
        """
        self.rules: list[SymptomRule] = rules or []
        self.exclude_overlaps: bool = exclude_overlaps

    def _is_more_specific(self, rule_a: SymptomRule, rule_b: SymptomRule) -> bool:
        """
        Determine if rule_a is more specific than rule_b.

        Args:
            rule_a: The first rule.
            rule_b: The second rule.

        Returns:
            True if rule_a is more specific than rule_b, False otherwise.
        """
        if rule_a.conditions and rule_b.conditions:
            return rule_a.conditions >= rule_b.conditions
        return False

    def _exclude_overlaps(
        self, applicable_rules: list[SymptomRule], rule: SymptomRule
    ) -> list[SymptomRule]:
        """
        Exclude overlapping rules that are less specific than the given rule.

        Args:
            applicable_rules: List of currently applicable rules.
            rule: The rule being evaluated.

        Returns:
            A filtered list of rules excluding less specific overlapping rules.
        """
        filtered_rules = []
        for r in applicable_rules:
            if self._is_more_specific(rule, r):
                continue
            elif self._is_more_specific(r, rule):
                filtered_rules.append(r)
            else:
                filtered_rules.append(r)
        return filtered_rules

    def add_rule(self, rule: SymptomRule) -> SymptomRule:
        """
        Add a new rule to the ruleset.

        Args:
            rule: The SymptomRule object to add.

        Returns:
            The added SymptomRule object.
        """
        if self.get_rule(rule.name):
            raise ValueError(f"A rule with the name '{rule.name}' already exists.")
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
        Return all rules that apply to the provided data, ensuring that overlapping
        rules with less specific conditions are excluded.

        Args:
            data: Input data to evaluate. Can be of any type.

        Returns:
            A list of applicable rules.
        """
        applicable_rules: list[SymptomRule] = []

        for rule in self.rules:
            if rule.applies(data):
                if self.exclude_overlaps:
                    applicable_rules = self._exclude_overlaps(applicable_rules, rule)
                applicable_rules.append(rule)

        return applicable_rules

    def list_rules(self) -> list[str]:
        """
        List the names of all rules in the ruleset.

        Returns:
            A list of rule names.
        """
        return [rule.name for rule in self.rules]
