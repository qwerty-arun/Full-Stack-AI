from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username: str

    @field_validator('username')
    def username_length(cls, v):
        if len(v) < 4:
            raise ValueError("Username must be atleast 4 characters")
        return v
    
    # raw username is cleaned up before Pydantic even checks types
    @model_validator(mode="before")
    def strip_and_fix(cls, data):
        # data is a dict with raw input
        data["username"] = data["username"].strip().lower()
        return data
    
class SignupData(BaseModel):
    password: str
    confirm_password: str

    # check or modify the whole object after all the fields are validated.
    @model_validator(mode='after')
    def password_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError("Password do not match")
        return values

# User(username="Ar")   # ❌ Raises ValueError
u = User(username="   Arun   ") # ✅ Works
print(u)

# SignupData(password="1234", confirm_password="123") # ❌ Raises ValueError
SignupData(password="1234", confirm_password="1234") # ✅ Works

"""
🔑 Summary
before = fix/normalize input data (dict level) before field validation.
after = validate or adjust the model object after field validation.
"""