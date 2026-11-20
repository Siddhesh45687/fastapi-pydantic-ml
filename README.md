# 🚀 FastAPI & Pydantic: Complete Hands-On Tutorial & ML Deployment

A comprehensive, project-driven repository taking you from **Python data validation with Pydantic v2** to building **production-ready REST APIs with FastAPI** and deploying an **end-to-end Machine Learning web application** with Streamlit.

---

## 📌 Project Overview

This repository is structured into three progressive learning modules:

1. **Pydantic Foundations & Schema Engineering**: Type safety, field-level constraints, custom validators (`@field_validator`), cross-field validation (`@model_validator`), nested schemas, serialization, and dynamic derived attributes using `@computed_field`.
2. **Patient Management REST API (CRUD)**: A complete patient record management system featuring query/path parameters, structured error handling (`HTTPException`), automatic BMI and clinical verdict computation, and JSON persistence.
3. **Machine Learning Model Serving & Frontend Integration**: A production-grade ML prediction microservice powered by FastAPI that serves a Scikit-Learn Random Forest pipeline for insurance premium category classification, paired with an interactive **Streamlit** dashboard.

---

## 📂 Project Structure

```plaintext
FastAPI_Tutorial/
├── 📄 app.py                              # FastAPI ML serving backend (Insurance Premium Predictor)
├── 📄 frontend.py                         # Streamlit interactive UI for the ML predictor
├── 📄 main.py                             # FastAPI introduction (GET routes, Path/Query params, sorting)
├── 📄 post.py                             # Full Patient Management CRUD API (GET, POST, PUT, DELETE)
├── 📄 patients.json                       # JSON database store for patient records
├── 📦 model (2).pkl                       # Trained Scikit-Learn Pipeline (RandomForest + ColumnTransformer)
│
├── 📁 pydantic_toturial/
│   └── 📄 pydantic_why.py                 # Motivation for Pydantic (manual validation vs Pydantic)
│
├── 📄 pydantic_demo.py                    # Schema definitions, Field constraints, Annotated, EmailStr, AnyUrl
├── 📄 field_validator.py                  # Field-level validators and transformers (@field_validator)
├── 📄 model_validator.py                  # Multi-field relational validation (@model_validator)
├── 📄 computed_fields.py                  # Dynamic derived fields (@computed_field)
├── 📄 nested_models.py                    # Complex nested data structures
├── 📄 serialization.py                    # Model export & filtering (model_dump_json, include/exclude)
│
└── 📄 FastAPI_Complete_Tutorial_Notes.pdf # Complete tutorial companion notes
```

---

## 🛠️ Tech Stack & Dependencies

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/) (`BaseModel`, `Field`, `computed_field`, `field_validator`, `model_validator`, `EmailStr`)
- **Web Server**: [Uvicorn](https://www.uvicorn.org/)
- **Frontend Dashboard**: [Streamlit](https://streamlit.io/)
- **Machine Learning**: [Scikit-Learn](https://scikit-learn.org/) (`Pipeline`, `RandomForestClassifier`, `ColumnTransformer`, `OneHotEncoder`)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **HTTP Client**: [Requests](https://requests.readthedocs.io/)

---

## 🚀 Getting Started

### 1. Clone the Repository & Set Up Virtual Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd FastAPI_Tutorial

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate
```

### 2. Install Required Dependencies

```bash
pip install fastapi uvicorn pydantic email-validator streamlit requests pandas scikit-learn
```

---

## 📖 Modules & Code Walkthrough

### Module 1: Pydantic & Data Validation

Explore modern Python data validation patterns:
- **`pydantic_why.py`**: Compares cumbersome manual `if-else` and `isinstance` checks against clean schema definitions.
- **`pydantic_demo.py`**: Demonstrates `Field` metadata, limits (`gt`, `lt`), `EmailStr`, `AnyUrl`, and `Annotated` types.
- **`field_validator.py`**: Custom domain checks (e.g., verifying corporate email domains like `@hdfc.com`) and data transformation (e.g., auto-capitalizing names).
- **`model_validator.py`**: Cross-attribute dependencies (e.g., requiring an emergency contact if a patient is over 60 years old).
- **`computed_fields.py`**: Computes BMI automatically from height and weight without requiring user input.
- **`nested_models.py` & `serialization.py`**: Models inside models (`Address` inside `Patient`) and JSON exports.

To run any Pydantic script:
```bash
python field_validator.py
python model_validator.py
```

---

### Module 2: Patient Management CRUD System (`post.py` & `main.py`)

A fully functional RESTful API managing medical patient records stored in `patients.json`.

#### Key Features:
- **Automatic Health Metrics**: Calculates `bmi` and health `verdict` (`Underweight`, `Normal`, `Obese`) on creation and update.
- **Partial Updates**: Uses `PatientUpdate` with `exclude_unset=True` to allow selective field edits without overwriting existing data.
- **Validation**: Enforces strict numeric bounds, enumerated values (`Literal['male', 'female', 'others']`), and sensible query options.

#### Run the Patient API:
```bash
uvicorn post:app --reload --port 8000
```
Interactive Swagger UI will be available at: **`http://127.0.0.1:8000/docs`**

#### API Endpoints Reference:
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status check |
| `GET` | `/about` | Overview of the service |
| `GET` | `/view` | Retrieve all patient records |
| `GET` | `/patient/{patient_id}` | Retrieve patient by unique ID |
| `GET` | `/sort?sort_by=bmi&order=desc` | Sort patients by `height`, `weight`, or `bmi` |
| `POST` | `/create` | Add a new patient record with automatic BMI calculation |
| `PUT` | `/edit/{patient_id}` | Partially update an existing patient record |
| `DELETE` | `/delete/{patient_id}` | Remove a patient from the database |

---

### Module 3: End-to-End ML Deployment (`app.py` + `frontend.py`)

A full-stack machine learning application predicting **Health Insurance Premium Category**.

#### How it Works:
1. **Feature Engineering on the Fly**:
   The `UserInput` Pydantic model computes:
   - `bmi`: Calculated from raw height and weight.
   - `lifestyle_risk`: Categorized (`low`, `medium`, `high`) based on smoking status and BMI.
   - `age_group`: Categorized (`young`, `adult`, `middle_aged`, `senior`).
   - `city_tier`: Maps 50+ Indian cities into Tier 1, Tier 2, or Tier 3.
2. **Inference Pipeline**:
   Features are formatted into a Pandas DataFrame and passed into the pre-trained `Pipeline(OneHotEncoder + RandomForestClassifier)`.
3. **Rich Response**:
   Returns the predicted category, max prediction confidence, and probability breakdown across all categories.

#### Run the ML Backend & Frontend:

**Terminal 1 (Backend API):**
```bash
uvicorn app:app --reload --port 8000
```

**Terminal 2 (Streamlit UI):**
```bash
streamlit run frontend.py
```

Open `http://localhost:8501` to use the insurance premium prediction web application!

---

## 🧪 Interactive API Documentation

FastAPI automatically generates interactive OpenAPI documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Test endpoints directly in your browser.
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) — Clean, comprehensive documentation layout.

---

## 💡 Best Practices Demonstrated

- ✅ **Type Hints & Static Analysis**: Leveraging Python type hints with Pydantic for run-time validation and self-documenting code.
- ✅ **Computed Fields**: Eliminating redundant client-side calculations using `@computed_field`.
- ✅ **Decoupled Architecture**: Clean separation between model training artifacts, backend API inference, and frontend presentation.
- ✅ **Robust Error Handling**: Descriptive HTTP status codes (`400 Bad Request`, `404 Not Found`, `201 Created`).
