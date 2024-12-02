from typing import Any, Optional

from pydantic import BaseModel


class DiagnosisBase(BaseModel, extra="allow"):
    """
    Base class for evaluation results. Allows default fields and additional \
    customization.
    """

    total_score: Optional[float] = None
    label: Optional[str] = None
    confidence: Optional[float] = None


class Diagnosis(DiagnosisBase):
    """
    Represents the result of an evaluation process. Can extend DiagnosisBase.
    """

    metadata: Optional[dict[str, Any]] = None
