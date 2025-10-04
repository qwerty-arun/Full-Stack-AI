"""
Form Data Validation CLI
---------------------------------
Validates CSV or JSON files using Pydantic.
Highlights invalid rows (wrong email format, missing fields, etc.)
"""

from pydantic import BaseModel, Field, ConfigDict, model_validator
import json
import csv
import os
import sys

# ---------------------------
# MODELS
# ---------------------------
class FormValidation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = Field(..., description="Full Name")
    email: str = Field(..., description="Email address (must contain @gmail.com)")
    phone: str = Field(..., description="Phone Number (10 digits)")

    @model_validator(mode="after")
    def validate_fields(cls, values):
        name = values.name.strip()
        email = values.email.strip()
        phone = values.phone.strip().replace("+91-", "").replace(" ", "")

        # Validate conditions
        if (
            name == ""
            or "@gmail.com" not in email
            or not phone.isdigit()
            or len(phone) != 10
        ):
            print(f"❌ Invalid -> 📕 {name or '(missing name)'} | ✉️ {email} | 📞 {phone}")
        return values


# ---------------------------
# FUNCTIONS
# ---------------------------
def validate_csv(path: str):
    print(f"\n📂 Validating CSV file: {path}\n{'-'*50}")
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                FormValidation(**row)
            except Exception as e:
                print(f"⚠️ Skipped row due to error: {e}")


def validate_json(path: str):
    print(f"\n📂 Validating JSON file: {path}\n{'-'*50}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

        # Handle both list of dicts or single dict
        if isinstance(data, dict):
            data = [data]

        for entry in data:
            try:
                FormValidation(**entry)
            except Exception as e:
                print(f"⚠️ Skipped entry due to error: {e}")


# ---------------------------
# MAIN CLI
# ---------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python form_validation_cli.py <path_to_file.csv/json>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        sys.exit(1)

    if path.endswith(".csv"):
        validate_csv(path)
    elif path.endswith(".json"):
        validate_json(path)
    else:
        print("⚠️ Unsupported file type. Please provide a .csv or .json file.")
