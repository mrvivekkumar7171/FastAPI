'''
A Pydantic model for validating the input from an user before make prediction.
'''

from pydantic import BaseModel, Field, computed_field, field_validator, EmailStr, AnyUrl, model_validator
from config.city_tier import tier_1_cities, tier_2_cities
from typing import Literal, Annotated, List, Dict, Optional

class Address(BaseModel):
    city: Annotated[Optional[str], Field(
        default=None, 
        description='City of the user',
        examples=['Delhi', 'Mumbai', 'Bangalore'])]
    state: Annotated[Optional[str], Field(
        default=None, 
        description='State of the user',
        examples=['New Delhi', 'Maharashtra', 'Jharkhand'])]
    pin: Annotated[Optional[int], Field(
        default=None, 
        description='PIN of the user',
        examples=[110047, 110074, 825402])]

    @field_validator('city', mode='before')
    @classmethod
    def normalize_city(cls, v:str) -> str:
        if isinstance(v, str):
            return v.strip().title()
        return v

class UserInput(BaseModel):

    name: Annotated[Optional[str], Field(
        max_length=50, 
        title='Name of the patient', 
        description='Give the name of the patient in less than 50 chars', 
        examples=['Vivek', 'Prabhat','Ayush'])] 
    age: Annotated[int, Field(
        ..., 
        gt=0, 
        lt=120, 
        description='Age of the user', 
        examples=[22, 45, 60])]
    height: Annotated[float, Field(
        ..., 
        gt=0, 
        lt=2.5, 
        description='Height of the user',
        examples=[1.65, 1.75, 1.80])]
    weight: Annotated[float, Field(
        ..., 
        gt=0, 
        strict=True, 
        description='Weight of the user',
        examples=[60.5, 75.0, 80.0])]
    income_lpa: Annotated[float, Field(
        ..., 
        gt=0, 
        description='Annual salary of the user in lpa',
        examples=[3.5, 10.0, 15.0])]
    smoker: Annotated[bool, Field(
        default=None, 
        description='Is user a smoker',
        examples=[False, True])]
    married: Annotated[Optional[bool], Field(
        default=None, 
        description='Is the patient married or not',
        examples=[False, True])] 
    occupation: Annotated[Literal['private_job','retired', 'freelancer', 'student', 'government_job',
        'business_owner', 'unemployed'], Field(
        default=None, 
        description='Occupation of the user',
        examples=['private_job', 'retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed'])]
    allergies: Annotated[Optional[List[str]], Field(
        default=None, max_length=5, 
        description='List of allergies of the user', 
        examples=[['Dust','Pollen'],['Peanuts','Milk'],['None']])] 
    email: Annotated[Optional[EmailStr],Field(
        default=None,
        examples=['mrvivekkumar7171@gmail.com'])]
    linkedin_url: Annotated[Optional[AnyUrl], Field(
        default=None,
        examples=['https://www.linkedin.com/in/Vivek-Kumar7171/'], 
        description='LinkedIn profile URL of the user')]
    address: Optional[Address]
    contact_details: Annotated[Optional[Dict[str, str]],Field(
        default=None,
        examples=[{"additionalProp1": "9087654321", "additionalProp2": "1234567890"}],
        description="Key-value pairs of contact-related data")]

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: EmailStr) -> EmailStr:
        valid_domains = ['hdfc.com','icici.com','sbi.com','axisbank.com','canarabank.com','gmail.com']
        domain_name = v.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return v.strip().lower()

    @field_validator('name')
    @classmethod
    def transform_name(cls, v: str) -> str:
        return v.upper()

    @field_validator('age', mode='before')
    def validate_age(cls, v):
        if not (0 < v < 100):
            raise ValueError('Age must be between 1 and 99')
        return v

    @model_validator(mode='after')
    def age_income_validator(cls,model):
        if model.age > 60 and model.income_lpa < 1000000:
            raise ValueError('Client above 60 years must have income more than 10 lpa')
        return model

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)
    
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
        if self.address.city in tier_1_cities:
            return 1
        elif self.address.city in tier_2_cities:
            return 2
        else:
            return 3

# # Example usage of the UserInput model
# data = {
#     "name": "Vivek",
#     "age": 22,
#     "height": 1.65,
#     "weight": 60.5,
#     "income_lpa": 3.5,
#     "smoker": False,
#     "married": False,
#     "occupation": "private_job",
#     "allergies": [
#         "Dust",
#         "Pollen"
#     ],
#     "email": "mrvivekkumar7171@gmail.com",
#     "linkedin_url": "https://www.linkedin.com/in/Vivek-Kumar7171/",
#     "address": {
#         "city": "Delhi",
#         "state": "New Delhi",
#         "pin": 110047
#     },
#     "contact_details": {
#         "additionalProp1": "9087654321",
#         "additionalProp2": "1234567890"
#     }
# }

# user1 = UserInput(**data)
# # is equivalent to:
# user1 = UserInput(name=data['name'],age=data['age'],height=data['height'], weight=data['weight'], income_lpa=data['income_lpa'], smoker=data['smoker'], married=data['married'], occupation=data['occupation'], allergies=data['allergies'],email=data['email'], linkedin_url=data['linkedin_url'], address=Address(**data['address']), contact_details=data['contact_details'])
# # print(user1.city_tier)
# # print(user1.age_group)
# # print(user1.lifestyle_risk)
# # print(user1.bmi)

# temp = user1.model_dump()
# # print(temp)
# temp = user1.model_dump(include=['age', 'weight'])
# # print(temp)
# temp = user1.model_dump(exclude=['age', 'weight'])
# # print(temp)
# temp = user1.model_dump(exclude={'address':['state']})
# # print(temp)
# temp = user1.model_dump(exclude_unset=True)
# # print(temp)
# # print(type(temp))

# temp = user1.model_dump_json()
# # print(temp)
# # print(type(temp))