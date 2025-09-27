from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool

    # error if below class is commented out
    class Config:
        validate_assignment = True

input_data = {'id': "108", 'name': "Arun", "is_active": True}

user = User(**input_data)
print(user)
user.id = "chai"
print(user)