'''
A Pydantic model for validating the input from an user before make prediction.
'''

from pydantic import BaseModel, Field, computed_field, field_validator, EmailStr, AnyUrl, model_validator
from config.city_tier import tier_1_cities, tier_2_cities
from typing import Literal, Annotated, List, Dict, Optional

# In FastAPI, a Response Model defines the structure of the data that your API endpoint will return. It helps in:
# 1. Generating clean API docs (/docs).
# 2. Validating output (so your API doesn't return malformed responses).
# 3. Filtering unnecessary data from the response.
# NOTE: like we validated user input the same we validate model output send to the user using the Response Model.

# Nested Models: If you have complex data structures, you can define nested Pydantic models to represent them. This allows you to create a structured response that can include other models as fields. It helps in better organization of related data, Reusability of common structures, Readability and Validation of complex data.
class Adddress(BaseModel):
    city: Annotated[Optional[str], Field(default='Aya Nagar', description='City of the user')]
    state: Annotated[Optional[str], Field(default='New Delhi', description='State of the user')]
    pin: Annotated[Optional[int], Field(default=110047, description='PIN of the user')]

# pydantic model to validate incoming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')] #NOTE It convert '30' to 30 automatically, while give error for 'thirty'.
    weight: Annotated[float, Field(..., gt=0, strict=True, description='Weight of the user')] # strict=True is used prohibit implicit conversion, so '30' will not be converted to 30.
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
        'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    name: Annotated[Optional[str], Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])] # Field and Annotated are used to add metadata (title, description and examples.) for API documentation.
    married: Annotated[Optional[bool], Field(default=None, description='Is the patient married or not')] # Field is used to add customer validation and default values.
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)] # By default, all fields in a Pydantic model are required. You can make fields optional by using `Optional` or by setting a default value.
    contact_details: Optional[Dict[str, str]] # It validates the dictionary keys and values as strings along with whole is dictionary.
    email: Annotated[Optional[EmailStr],Field(default='user@icici.com')] # built-in validator for email addresses, not just validate to be a string, but an actual email ID.
    linkedin_url: Optional[AnyUrl] # built-in validator for URLs.
    Adddress: Optional[Adddress] # Nested model to validate address.

    # field_validator is used to apply custom validation on the fields.
    @field_validator('email') # validation on email field
    @classmethod
    def validate_email(cls, v: EmailStr) -> EmailStr:
        valid_domains = ['hdfc.com','icici.com','sbi.com','axisbank.com','canarabank.com']
        domain_name = v.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return v.strip().lower()

    # @field_validator('name')
    @classmethod
    def transform_name(cls, v: str) -> str:
        return v.upper()

    # mode='before' means output will be of before field validation. If input is '30' then output will be error of '< is not supported between int and str.
    # mode='after' means output will be of after field validation. If input is '30' then output will be the value or Value error based on the condition 0 < v < 100.
    @field_validator('age', mode='before') # default mode is 'after'.
    def validate_age(cls, v):
        if not (0 < v < 100):
            raise ValueError('Age must be between 1 and 99')
        return v

    # model_validator is used to validate the whole model after all field validations are done.
    @model_validator(mode='after')
    def age_income_validator(cls,model):
        if model.age > 60 and model.income_lpa < 1000000:
            raise ValueError('Client above 60 years must have income more than 10 lpa')
        return model

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v:str) -> str:
        return v.strip().title()

    # computed_field is used to create a field that is computed based on other fields. Indirect use of user inputs.
    @computed_field
    @property
    def bmi(self) -> float: # name of the new computed field is same as the function name. here, it is bmi.
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
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


# # Example usage of the UserInput model
# data = {
#     "age": 1,
#     "weight": 1,
#     "height": 1,
#     "income_lpa": 1,
#     "smoker": True,
#     "city": "string",
#     "occupation": "retired",
#     "name": "Nitish",
#     "married": True,
#     "allergies": ["string"],
#     "contact_details": {
#         "additionalProp1": "string",
#         "additionalProp2": "string",
#         "additionalProp3": "string"
#     },
#     "email": "user@icici.com",
#     "linkedin_url": "https://example.com/",
#     "Adddress": {
#         "city": "Aya Nagar",
#         "state": "New Delhi",
#         "pin": 110047
#     }
# }

# print(UserInput(**data))
# # Output: age=1 weight=1.0 height=1.0 income_lpa=1.0 smoker=True city='String' occupation='retired' name='Nitish' married=True allergies=['string'] contact_details={'additionalProp1': 'string', 'additionalProp2': 'string', 'additionalProp3': 'string'} email='user@icici.com' linkedin_url=Url('https://example.com/') Adddress=Adddress(city='Aya Nagar', state='New Delhi', pin=110047) bmi=1.0 lifestyle_risk='medium' age_group='young' city_tier=3

# user1 = UserInput(age=data['age'], weight=data['weight'], height=data['height'], income_lpa=data['income_lpa'], smoker=data['smoker'], city=data['city'], occupation=data['occupation'],name=data['name'], married=data['married'], allergies=data['allergies'], contact_details=data['contact_details'], email=data['email'], linkedin_url=data['linkedin_url'], Adddress=Adddress(**data['Adddress']))
# print(user1.age)
# # Output: 1

# temp = user1.model_dump() # dictionary
# print(temp)
# temp = user1.model_dump(include=['age', 'weight']) # dictionary with only age and weight fields
# print(temp)
# temp = user1.model_dump(exclude=['age', 'weight']) # dictionary with all fields except age and weight
# print(temp)
# temp = user1.model_dump(exclude={'address':['state']}) # dictionary with all fields except state in address
# print(temp)
# temp = user1.model_dump(exclude_unset=True) # dictionary with only fields that are set (not default values)
# print(temp)
# print(type(temp))
# # Output: {"name":"Alice","age":25}
# # Output: <class 'dict'>
# # Output: {"age":1,"weight":1}
# # Output: {"height":1,"income_lpa":1,"smoker": true,"city": "string","occupation":"retired",  "name":"Nitish","married":true,"allergies":["string"],"contact_details":{"additionalProp1":"string",    "additionalProp2":"string","additionalProp3":"string"},"email":"user@icici.com","linkedin_url":"https://example.com/",  "Adddress":{"city":"Aya Nagar","state":"New Delhi","pin":"110047"}}
# # Output:{"age":1,"weight":1,"height":1,"income_lpa":1,"smoker": true,"city": "string","occupation":"retired",  "name":"Nitish","married":true,"allergies":["string"],"contact_details":{"additionalProp1":"string",    "additionalProp2":"string","additionalProp3":"string"},"email":"user@icici.com","linkedin_url":"https://example.com/",  "Adddress":{"city":"Aya Nagar","pin":"110047"}}

# temp = user1.model_dump_json() # JSON string (but type will be visible as str)
# print(temp)
# print(type(temp))
# # Output: {'name': 'Alice', 'age': 25}
# # Output: <class 'str'>