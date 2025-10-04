# Pydantic Projects to work on

## 🔹 Beginner Projects

- [x] **User Signup / Login Data Validation**

  - Validate fields like username, email, password.
  - Add checks (min length, regex for email, matching password confirmation).

- [x] **Configuration Manager**

  - Use `BaseSettings` to manage environment variables.
  - Example: database credentials, API keys, feature flags.

- [x] **JSON Schema Generator**

  - Define models and export their JSON Schema (`.model_json_schema()`).
  - Visualize how models translate to API contracts.

- [x] **Data Cleaning Utility**

  - Accept unstructured JSON (maybe from a file).
  - Parse into a clean `BaseModel` with strict typing (e.g., convert strings like `"42"` into ints).

---

## 🔹 Intermediate Projects

- [x] **REST API with FastAPI + Pydantic**

  - Use Pydantic models for request/response schemas.
  - Example: A simple **Task Manager API** with task creation, updates, and validations.

- [x] **Form Data Validation CLI**

  - Build a CLI tool that loads CSV/JSON files and validates rows with Pydantic.
  - Highlight invalid rows (e.g., wrong email format, missing fields).

- [ ] **Financial Data Validator**

  - Parse and validate transactions (amount, date, currency codes).
  - Add model validators for business logic (e.g., amount > 0, valid ISO currency).

- [ ] **IoT Sensor Data Parser**

  - Incoming sensor payloads (temperature, humidity, GPS).
  - Validate ranges (e.g., -50 < temp < 150).
  - Auto-convert timestamps into `datetime`.

---

## 🔹 Advanced Projects

- [ ] **Schema Migration Tool**

  - Compare old vs. new Pydantic models and highlight differences.
  - Example: field removed/renamed, type changed.

- [ ] **ETL Pipeline with Pydantic Models**

  - Extract raw data → Validate/transform with Pydantic → Load into DB.
  - Add logging for errors (invalid rows).

- [ ] **Custom Validation Framework**

  - Extend `@field_validator` and `@model_validator` for domain-specific rules.
  - Example: Healthcare data (blood pressure ranges, age constraints).

- [ ] **Pydantic + Kafka / RabbitMQ Consumer**

  - Consumer service reads JSON messages.
  - Validate against Pydantic models before processing.

- [ ] **Machine Learning Input Validator**

  - Define strict Pydantic schemas for model inputs (features).
  - Ensure values are within expected ranges (e.g., no negative ages, categorical values allowed only from a set).

- [ ] **GraphQL + Pydantic Models**

  - Use Pydantic to define input/output schemas for a GraphQL API.
  - Auto-generate docs from schemas.

---

# 🤖 ML-Focused Pydantic Projects

## **1. Dataset Schema Validator** (Beginner → Intermediate)

- Build Pydantic models for a dataset (e.g., Titanic dataset).
- Ensure all fields match expected types:

  - `age: int | None`
  - `sex: Literal["male", "female"]`
  - `fare: float >= 0`

- Add validation for missing values.
  ✅ Useful for: Cleaning Kaggle datasets before training.

---

## **2. ML Experiment Config Manager** (Intermediate)

- Define experiment configs in YAML/JSON:

  ```yaml
  learning_rate: 0.001
  batch_size: 32
  model: "resnet50"
  ```

- Use `BaseSettings` to parse them into strongly-typed configs.
- Validate ranges (e.g., `batch_size > 0`, `learning_rate <= 1`).
  ✅ Useful for: Running consistent ML experiments.

---

## **3. Feature Engineering Validator** (Intermediate → Advanced)

- Define schema for feature sets (e.g., house price prediction).
- Validate ranges: `square_feet > 0`, `year_built <= 2025`.
- Catch outliers before training.
  ✅ Useful for: Preventing bad data from polluting ML training.

---

## **4. ML Input Validator (Serving Stage)** (Advanced)

- Build an API (FastAPI + Pydantic) for ML inference.
- Schema enforces correct input at runtime:

  ```python
  class PredictInput(BaseModel):
      sepal_length: float
      sepal_width: float
      petal_length: float
      petal_width: float
  ```

- Reject invalid requests before they hit the model.
  ✅ Useful for: Safe ML deployments.

---

## **5. Model Prediction Tracker** (Advanced)

- Wrap ML predictions in a Pydantic model:

  ```python
  class Prediction(BaseModel):
      input: PredictInput
      output: float
      confidence: float
      timestamp: datetime
  ```

- Store results in DB / log file.
- Enforce confidence between `0 and 1`.
  ✅ Useful for: Monitoring deployed ML models.

---

## **6. Data Pipeline Validator for ETL** (Pro Level)

- Build a full **ETL pipeline** for ML data:

  - Extract: CSV/JSON datasets.
  - Transform: Validate & normalize features with Pydantic.
  - Load: Save clean dataset into SQLite/Postgres.

- Add logging for invalid rows.
  ✅ Useful for: Automating ML dataset preparation.

---
