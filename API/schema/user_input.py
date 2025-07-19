from pydantic import BaseModel, Field, computed_field, field_validator
from config.city_tier import tier_1_cities, tier_2_cities
from typing import Literal, Annotated

# In FastAPI, a Response Model defines the structure of the data that your API endpoint will return. It helps in:
# 1. Generating clean API docs (/docs).
# 2. Validating output (so your API doesn't return malformed responses).
# 3. Filtering unnecessary data from the response.
# NOTE: like we validated user input the same we validate model output send to the user using the Response Model.


# pydantic model to validate incoming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
        'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v:str) -> str:
        return v.strip().title()

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3