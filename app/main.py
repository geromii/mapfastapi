from fastapi import FastAPI
from pydantic import BaseModel
from utils import generate_function_calls
# Initialize FastAPI
app = FastAPI()

# Define your data model for Product
class Order(BaseModel):
    product: str
    units: int

class Product(BaseModel):
    name: str
    notes: str

class AIRequest(BaseModel):
    input: str

@app.get("/ok")
async def ok_endpoint():
    return {"message": "ok"}

@app.get("/hello")
async def hello_endpoint(name: str = 'World'):
    return {"message": f"Hello, {name}!"}

@app.post("/orders")
async def place_order(product: str, units: int):
    return {"message": f"Order for {units} units of {product} placed successfully."}

@app.post("/orders_pydantic")
async def place_order(order: Order):
    return {"message": f"Order for {order.units} units of {order.product} placed successfully."}


@app.post("/ai_function")
async def generate_ai_functions(request: AIRequest):
    description = generate_function_calls(request.input)
    return {"product_description": description}

