import pickle
import pandas as pd

# import the ml model
with open('models/model.pkl', 'rb') as f:
    model = pickle.load(f)

# version of the model: generally model version came from mlflow or any other model management system
MODEL_VERSION = '1.0.0'

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]

    confidence = max(probabilities)

    # to display more information from the model output result (optional must required for professional projects)
    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }