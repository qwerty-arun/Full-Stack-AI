"""
🟢 1. GET → Retrieve Data (Read)

Purpose:
Used to fetch or read data from the server.
No data is modified — it’s only for retrieving information.
"""

"""
How it works:

-   If you visit http://127.0.0.1:8000/items/1,
    → FastAPI returns the item with ID 1.

✅ Used for: reading data.
🚫 Do not send sensitive data in query parameters.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": "Laptop", "price": 1000}
