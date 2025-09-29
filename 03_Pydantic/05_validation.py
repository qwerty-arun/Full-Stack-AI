from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username: str
    age: int

    @model_validator(mode="before")
    def before_model(cls, data):
        print("🔹 model_validator BEFORE called")
        return data

    @field_validator("username")
    def validate_username(cls, v):
        print("🔹 field_validator for username called")
        return v

    @model_validator(mode="after")
    def after_model(self):
        print("🔹 model_validator AFTER called")
        return self


u = User(username="Arun", age=25)
