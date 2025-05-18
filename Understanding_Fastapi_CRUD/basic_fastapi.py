from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ------------------ MODULE 1: Introduction to FastAPI ------------------

# FastAPI app metadata
app = FastAPI(
    title="Shanmugavel FastAPI",
    description="Podaa edu en koda...",
    version="5.6.0"
)

# In-memory data (list of product dictionaries)
items = [
    {"name": "Laptop", "price": 45000, "desc": "High-performance laptop for work and gaming"},
    {"name": "Smartphone", "price": 15000, "desc": "Latest model smartphone with AMOLED display"},
    {"name": "Headphones", "price": 3000, "desc": "Wireless over-ear noise cancelling headphones"},
    {"name": "Keyboard", "price": 1200, "desc": "Mechanical keyboard with RGB lighting"},
    {"name": "Monitor", "price": 9000, "desc": "24-inch Full HD monitor for productivity"}
]

# ------------------ MODULE 2: Basics ------------------

# Create a product schema using Pydantic
class Product(BaseModel):
    name: str
    price: int
    desc: str

# ------------------ MODULE 3: API Documentation ------------------

# FastAPI automatically provides Swagger at /docs and Redoc at /redoc
# We can improve docs with `tags`, `summary`, and `response_model`

# ------------------ MODULE 1: Introduction Routes ------------------

@app.get("/", tags=["Basic"], summary="Home endpoint")
def home():
    return {"message": "Welcome to Shanmugavel's FastAPI project!"}

@app.get("/product", tags=["Basic"], summary="Product information")
def product():
    return {"data": "currently you are in product data"}

@app.get("/services", tags=["Basic"], summary="Services information")
def get_services():
    return {"data": "currently you are in services data"}

@app.get("/services/{id}", tags=["Logic"], summary="Get specific service by ID")
def get_service_by_id(id: int):
    # Math logic: double the id and add 10
    result = id * 2 + 10
    return {"original_id": id, "calculated_value": result}


# Dynamic path parameters with math logic
@app.get("/bonus/{basesalary}/{bonus}", tags=["Logic"], summary="Calculate bonus amount")
def calculate_bonus(basesalary: int, bonus: int):
    return {"data": basesalary + bonus}

# ------------------ MODULE 4: CRUD OPERATIONS ------------------

# Create product (only return confirmation, no saving)
@app.post("/product", tags=["Products"], summary="Receive product data")
def new_product(pro: Product):
    return {"message": f"Product '{pro.name}' received successfully"}

# Create product and add to list (in-memory DB)
@app.post("/create_product", status_code=201, tags=["Products"], summary="Create a new product")
def create_product(pro: Product):
    item_data = {"name": pro.name, "price": pro.price, "desc": pro.desc}
    items.append(item_data)
    return {"message": "Product added successfully", "products": items}

# Read all products
@app.get("/view_all_product", tags=["Products"], summary="View all products")
def view_all_products():
    return items

# Read one product by price
@app.get("/view_product/{price_val}", tags=["Products"], summary="View product by price")
def view_single_product(price_val: int):
    for i in items:
        if i["price"] == price_val:
            return {"name": i["name"], "desc": i["desc"], "price": i["price"]}
    raise HTTPException(status_code=404, detail="Product Not Found")

# Update product by price
@app.put("/update_product/{price_val}", tags=["Products"], summary="Update product by price")
def update_product(price_val: int, pro: Product):
    for i in items:
        if i["price"] == price_val:
            i["name"] = pro.name
            i["price"] = pro.price
            i["desc"] = pro.desc
            return {"message": "Product updated successfully", "updated_product": i}
    # Module 5 - Error Handling
    raise HTTPException(status_code=404, detail="Product Not Found")

# Delete product by price
@app.delete("/delete_product/{price_val}", tags=["Products"], summary="Delete product by price")
def delete_product(price_val: int):
    for i in items:
        if i["price"] == price_val:
            items.remove(i)
            return {"message": "Product deleted successfully"}
    # Module 5 - Error Handling
    raise HTTPException(status_code=404, detail="Product Not Found")