"""
🟡 2. POST → Create Data (Create)

Purpose:
Used to send new data to the server — typically to create a new record.
"""
from pydantic import BaseModel
from fastapi import FastAPI

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created", "item": item}

"""
How it works:

Send a POST request with JSON data (e.g., via Postman or a frontend form):

{
  "name": "Phone",
  "price": 800
}


→ The endpoint processes and returns the created data.

✅ Used for: creating new resources.
"""