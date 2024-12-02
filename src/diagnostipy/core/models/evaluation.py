from pydantic import BaseModel


class BaseEvaluation(BaseModel):
    """
    Base model for evaluation results.

    All evaluation models must include:
        - label (str): The evaluation label.
        - score (float): The total score of the evaluation.
    """

    label: str
    score: float
