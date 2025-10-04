"""
User Signup / Login Data Validation
- Validate fields like username, email, password.
- Add checks (min length, email, matching password confirmation).
"""

from pydantic import BaseModel, field_validator, model_validator, Field, EmailStr
import string

class SignUp(BaseModel):
    username: str = Field(
        ...,
        min_length=6,
        description="Username",
        examples="arunkr2004"
    )
    email:              EmailStr
    password:           str
    confirm_password:   str

    @field_validator('username')
    def username_length(cls, value):
        if len(value) < 6:
            raise ValueError("Username must be atleast 6 characters in length")
        return value
    
    @field_validator('email')
    def valid_email(cls, value):
        if value.find("@gmail.com") == -1:
            raise ValueError("Email should contain '@gmail.com'")
        return value
    
    @field_validator('password')
    def password_strength(cls, password):
        if len(password) < 8:
            raise ValueError("Password should contain 8 characters")
        if not any(c.islower() for c in password):
            raise ValueError("Password is missing a lowercase letter")
        if not any(c.isupper() for c in password):
            raise ValueError("Password is missing a uppercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password is missing a number")
        if not any(c in string.punctuation  for c in password):
            raise ValueError("Password is missing a special character")
        return password
    
    @model_validator(mode='after')
    def password_confirmation(cls, values):
        if values.password != values.confirm_password:
            raise ValueError("Passwords don't match")
        return values

user = SignUp(username="arunkr", email="arun@gmail.com", password="arunKR2004@", confirm_password="arunKR2004@")
print(user)