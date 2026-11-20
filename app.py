
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
from pathlib import Path
import pickle
import pandas as pd

# Load ML model
MODEL_PATH = Path(__file__).resolve().parent / "model (2).pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

app = FastAPI(
    title="Insurance Premium Category Predictor",
    description="Predict insurance premium category using ML",
    version="1.0"
)

# City categories
tier_1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow",
    "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat",
    "Rajkot", "Jodhpur", "Raipur", "Amritsar",
    "Varanasi", "Agra", "Dehradun", "Mysore",
    "Jabalpur", "Guwahati", "Thiruvananthapuram",
    "Ludhiana", "Nashik", "Allahabad", "Udaipur",
    "Aurangabad", "Hubli", "Belgaum", "Salem",
    "Vijayawada", "Tiruchirappalli", "Bhavnagar",
    "Gwalior", "Dhanbad", "Bareilly", "Aligarh",
    "Gaya", "Kozhikode", "Warangal", "Kolhapur",
    "Bilaspur", "Jalandhar", "Noida", "Guntur",
    "Asansol", "Siliguri"
]


# Pydantic input model
class UserInput(BaseModel):

    age: Annotated[
        int,
        Field(gt=0, lt=120, description="Age of the user")
    ]

    weight: Annotated[
        float,
        Field(gt=0, description="Weight of the user")
    ]

    height: Annotated[
        float,
        Field(gt=0, lt=2.5, description="Height of the user")
    ]

    income_lpa: Annotated[
        float,
        Field(gt=0, description="Annual income in LPA")
    ]

    smoker: Annotated[
        bool,
        Field(description="Is the user a smoker?")
    ]

    city: Annotated[
        str,
        Field(min_length=1, description="User's city")
    ]

    occupation: Literal[
        'retired',
        'freelancer',
        'student',
        'government_job',
        'business_owner',
        'unemployed',
        'private_job'
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:

        if self.smoker and self.bmi > 30:
            return "high"

        elif self.smoker or self.bmi > 27:
            return "medium"

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

        city = self.city.strip().casefold()

        tier_1 = {c.casefold() for c in tier_1_cities}
        tier_2 = {c.casefold() for c in tier_2_cities}

        if city in tier_1:
            return 1

        elif city in tier_2:
            return 2

        return 3


# Home route
@app.get("/")
def home():
    return {
        "message": "Insurance Premium Predictor API is running"
    }


# Prediction route
@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    # Prediction
    prediction = model.predict(input_df)[0]

    confidence = None
    class_probabilities = {}

    # Probability calculation
    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_df)[0]

        classes = model.classes_

        class_probabilities = {
            str(label): float(probability)
            for label, probability in zip(classes, probabilities)
        }

        confidence = float(max(probabilities))

    return {
        "response": {
            "predicted_category": str(prediction),
            "confidence": confidence,
            "class_probabilities": class_probabilities
        }
    }

        