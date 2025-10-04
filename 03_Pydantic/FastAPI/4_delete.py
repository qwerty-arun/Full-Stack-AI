"""
🔴 4. DELETE → Remove Data (Delete)

Purpose:
Used to delete a resource from the server.
"""

from pydantic import BaseModel
from fastapi import FastAPI

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

"""
How it works:

DELETE /items/1
→ The item with ID 1 is removed.

✅ Used for: deleting resources.
"""