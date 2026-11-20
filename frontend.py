
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    value=30
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    value=65.0
)

height = st.number_input(
    "Height (m)",
    min_value=0.5,
    max_value=2.5,
    value=1.7
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    value=10.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    options=[True, False]
)

city = st.text_input("City", value="Mumbai")

occupation = st.selectbox(
    "Occupation",
    [
        'retired',
        'freelancer',
        'student',
        'government_job',
        'business_owner',
        'unemployed',
        'private_job'
    ]
)

# Prediction
if st.button("Predict Premium Category"):

    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:

        with st.spinner("Predicting..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=10
            )

        if response.status_code == 200:

            result = response.json()
            prediction = result["response"]

            st.success(
                f"Predicted Insurance Premium Category: "
                f"{prediction['predicted_category']}"
            )

            confidence = prediction.get("confidence")

            if confidence is not None:
                st.metric(
                    "Prediction Confidence",
                    f"{confidence * 100:.2f}%"
                )
            else:
                st.info("Confidence score is not available.")

            probabilities = prediction.get(
                "class_probabilities", {}
            )

            if probabilities:
                st.subheader("Class Probabilities")

                for category, probability in probabilities.items():
                    st.write(f"{category}: {probability * 100:.2f}%")
                    st.progress(probability)

        else:

            st.error(f"API Error: {response.status_code}")

            try:
                st.json(response.json())
            except ValueError:
                st.write(response.text)

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI server. "
            "Please start the backend."
        )

    except requests.exceptions.Timeout:

        st.error("API request timed out.")

    except (ValueError, KeyError, TypeError) as e:

        st.error(f"Invalid API response: {e}")

    except requests.exceptions.RequestException as e:

        st.error(f"Request error: {e}")

