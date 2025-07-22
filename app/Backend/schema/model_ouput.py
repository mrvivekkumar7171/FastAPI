'''
A Pydantic model for validating and structuring the output of a machine learning prediction.
'''

from pydantic import BaseModel, Field
from typing import Dict

class ModelOutput(BaseModel):
    predicted_category: str = Field(
        ...,
        description="The predicted insurance premium category",
        examples=["High","Low","Medium"]
    ),
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted class (range: 0 to 1)",
        examples=[0.8432, 0.2123, 0.5789]
    ),
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        examples=[{"Low": 0.01, "Medium": 0.15, "High": 0.84},{"Low": 0.70, "Medium": 0.20, "High": 0.10},{"Low": 0.30, "Medium": 0.50, "High": 0.20}]
    )