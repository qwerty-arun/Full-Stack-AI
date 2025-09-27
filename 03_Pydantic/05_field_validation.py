from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username: str

    @field_validator('username')
    def username_length(cls, v):
        if len(v) < 4:
            raise ValueError("Username must be atleast 4 characters")
        return v
    
class SignupData(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def password_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError("Password do not match")
        return values

# User(username="Ar")   # ❌ Raises ValueError
User(username="Arun") # ✅ Works

# SignupData(password="1234", confirm_password="123") # ❌ Raises ValueError
SignupData(password="1234", confirm_password="1234") # ✅ Works