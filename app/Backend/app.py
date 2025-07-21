'''This FastAPI application provides an API for predicting insurance premium categories based on user input using a trained machine learning model.
'''

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput # Input type validation
from models.predict import predict_output, MODEL_VERSION, model
from schema.model_ouput import ModelOutput # Output type validation

app = FastAPI()

# to tell the user that the API is working fine: for Humans
@app.get('/')
def home():
    return {'message':'Insurance Premium Category Prediction API'}

# to tell the aws that the API is healthy and working fine: for machine readable
@app.get('/health')
def health_check():
    return JSONResponse(status_code=200, content={'status': 'OK', 
                                                'model_version': MODEL_VERSION, 
                                                'model_loaded': model is not None})

# here, we are using post method specially when writing ML model or DL model APIs in FastAPI then must use post method
@app.post('/predict', response_model=ModelOutput) # response_model=PredictionOutput will validate first then send the user the output
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    # try statement to handle error if the model fails to predict or any other issue occurs
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})