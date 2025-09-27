from typing import List, Optional
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address

address = Address(
    street="123 Something",
    city="Bengaluru",
    postal_code="000000"
)

user = User(
    id=1,
    name="Arun",
    address=address
)

user_data = {
    "id": 1,
    "name": "Arun",
    "address": {
        "street": "321 something",
        "city": "Paris",
        "postal_code": "000001"
    }
}

user = User(**user_data)
print(user)