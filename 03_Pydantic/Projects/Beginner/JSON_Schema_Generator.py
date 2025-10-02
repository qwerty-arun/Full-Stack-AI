"""
JSON Schema Generator
   - Define models and export their JSON Schema (`.model_json_schema()`).
   - Visualize how models translate to API contracts.

Visualizing part:
This part means: once you generate the schema, you can see how it looks when used in an API definition (like OpenAPI/Swagger).

In other words, your Pydantic models don’t just validate Python objects — they can also define request/response bodies for APIs. Frameworks like FastAPI use Pydantic under the hood and automatically generate API contracts (OpenAPI docs) from your models.
"""

# To run this file: uvicorn JSON_Schema_Generator:app --reload

from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
class User(BaseModel):
    name: str
    age: int
    email: str | None = None

@app.post("/users/")
def create_user(user: User):
    return user

# print(User.model_json_schema())

"""
🔹 What’s going on when I said “visit /docs and see Swagger UI”?

FastAPI is a Python web framework that uses Pydantic models to define what data your API endpoints expect and return.

When you run a FastAPI app, it automatically:

Converts your Pydantic models into OpenAPI schemas (which is just JSON Schema + metadata).

Provides a visual interface (Swagger UI) at http://127.0.0.1:8000/docs.

This lets you (or anyone using your API) interactively test endpoints and see the API contract.


🔹 What happens when you open browser at:

http://127.0.0.1:8000/docs → Swagger UI

You’ll see an interactive page with your /users/ endpoint.

It will show that the request body must match the User Pydantic model (with id, name, email).

You can actually click “Try it out”, enter JSON, and hit “Execute”.

http://127.0.0.1:8000/openapi.json → raw OpenAPI schema

This is basically the collection of all JSON Schemas generated from your Pydantic models.


🔹 Why is this “visualizing API contracts”?

Without FastAPI, your schema is just raw JSON.

With FastAPI, that schema is turned into a visual contract (docs) where:

Developers see what’s required.

They can test APIs.

The schema is always up-to-date with your code.

👉 So, the second part of your challenge is really about taking your Pydantic models, turning them into schemas, and then seeing how those schemas define real-world API requests/responses.
"""