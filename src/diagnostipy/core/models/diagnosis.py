from typing import Any, Optional

from pydantic import BaseModel

from diagnostipy.core.models.symptom_rule import SymptomRule


class DiagnosisBase(BaseModel):
    pass


class Diagnosis(DiagnosisBase):
    """
    Represents the result of an evaluation process.

    Attributes:
        total_score (float): The total score calculated from applicable rules.
        label (Optional[str]): The label assigned to the evaluation result.
        confidence (Optional[float]): The confidence level of the evaluation.
    """

    total_score: float = 0.0
    label: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Optional[dict[str, Any]] = None
