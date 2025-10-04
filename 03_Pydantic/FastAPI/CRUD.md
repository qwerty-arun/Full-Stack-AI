## In **FastAPI**, the HTTP methods — **GET**, **POST**, **PUT**, and **DELETE** — correspond to the standard **CRUD** operations (Create, Read, Update, Delete).


---

### 🟢 1. `GET` → Retrieve Data (Read)

**Purpose:**
Used to **fetch** or **read** data from the server.
**No data is modified** — it’s only for retrieving information.

**Example:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": "Laptop", "price": 1000}
```

**How it works:**

* If you visit `http://127.0.0.1:8000/items/1`,
  → FastAPI returns the item with ID `1`.

✅ **Used for:** reading data.
🚫 **Do not** send sensitive data in query parameters.

---

### 🟡 2. `POST` → Create Data (Create)

**Purpose:**
Used to **send** new data to the server — typically to **create a new record**.

**Example:**

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created", "item": item}
```

**How it works:**

* Send a `POST` request with JSON data (e.g., via Postman or a frontend form):

```json
{
  "name": "Phone",
  "price": 800
}
```

→ The endpoint processes and returns the created data.

✅ **Used for:** creating new resources.

---

### 🔵 3. `PUT` → Update Data (Update)

**Purpose:**
Used to **replace or update** existing data.
Usually expects the **entire object** to be sent again (not just one field).

**Example:**

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"message": f"Item {item_id} updated", "item": item}
```

**How it works:**

* `PUT /items/1` with body:

```json
{
  "name": "Updated Laptop",
  "price": 1200
}
```

→ The item with ID 1 is replaced with the new data.

✅ **Used for:** full updates (replace existing resource).
🟠 If you only want to update part of an object, you use `PATCH`.

---

### 🔴 4. `DELETE` → Remove Data (Delete)

**Purpose:**
Used to **delete** a resource from the server.

**Example:**

```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
```

**How it works:**

* `DELETE /items/1`
  → The item with ID 1 is removed.

✅ **Used for:** deleting resources.

---

### ⚙️ Summary Table

| HTTP Method | CRUD Action | Description               | Request Body | Safe | Idempotent |
| ----------- | ----------- | ------------------------- | ------------ | ---- | ---------- |
| **GET**     | Read        | Retrieve resource         | ❌ No         | ✅    | ✅          |
| **POST**    | Create      | Create new resource       | ✅ Yes        | ❌    | ❌          |
| **PUT**     | Update      | Replace existing resource | ✅ Yes        | ❌    | ✅          |
| **DELETE**  | Delete      | Remove resource           | ❌ No         | ❌    | ✅          |

---

# Complete CRUD Example
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Data Model ---
class Item(BaseModel):
    id: int
    name: str
    price: float

# --- In-Memory "Database" ---
items_db = []

# --- CREATE (POST) ---
@app.post("/items/")
def create_item(item: Item):
    # Check if ID already exists
    for existing_item in items_db:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    items_db.append(item)
    return {"message": "Item created successfully", "item": item}


# --- READ ALL (GET) ---
@app.get("/items/")
def get_all_items():
    return {"items": items_db}


# --- READ ONE (GET by ID) ---
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# --- UPDATE (PUT) ---
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return {"message": "Item updated successfully", "item": updated_item}
    raise HTTPException(status_code=404, detail="Item not found")


# --- DELETE (DELETE) ---
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(index)
            return {"message": "Item deleted successfully", "item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")

```