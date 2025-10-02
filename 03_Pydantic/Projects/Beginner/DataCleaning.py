"""
Data Cleaning Utility
   - Accept unstructured JSON (maybe from a file).
   - Parse into a clean `BaseModel` with strict typing (e.g., convert strings like `"42"` into ints).
"""

from pydantic import BaseModel, field_validator, ConfigDict
import re
import json

class StructuredJSON(BaseModel):
    model_config = ConfigDict(extra="ignore")  # ignore unknown fields

    id: int
    name: str
    age: int
    is_active: bool

    @field_validator("id", mode="before")
    def parse_id(cls, v):
        return int(v)

    @field_validator("name", mode="before")
    def strip_name(cls, v):
        return v.strip()

    @field_validator("age", mode="before")
    def parse_age(cls, v):
        # Extract first number found in the string
        match = re.search(r"\d+", str(v))
        return int(match.group()) if match else 0

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, v):
        if str(v).lower() in {"yes", "true", "1"}:
            return True
        if str(v).lower() in {"no", "false", "0"}:
            return False
        raise ValueError(f"Invalid boolean value: {v}")


with open("data.json", "r") as f:
    unstructured_json = json.load(f)

cleaned = StructuredJSON(**unstructured_json)
print(cleaned.model_dump())