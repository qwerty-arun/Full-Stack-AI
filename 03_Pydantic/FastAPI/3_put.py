"""
🔵 3. PUT → Update Data (Update)

Purpose:
Used to replace or update existing data.
Usually expects the entire object to be sent again (not just one field).
"""
from pydantic import BaseModel
from fastapi import FastAPI

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"message": f"Item {item_id} updated", "item": item}

"""
How it works:

PUT /items/1 with body:

{
  "name": "Updated Laptop",
  "price": 1200
}


→ The item with ID 1 is replaced with the new data.

✅ Used for: full updates (replace existing resource).
🟠 If you only want to update part of an object, you use PATCH.
"""