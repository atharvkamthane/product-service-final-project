"""REST API and browser routes for the Product Service."""
from flask import jsonify, render_template, request
from service import app
from service.models import Product


def _product_values(data, existing=None):
    """Build validated Product field updates from request data."""
    existing = existing or {}
    values = {}
    for field in ("name", "description", "category", "available", "price"):
        if field not in data:
            continue
        value = data[field]
        if field == "available" and not isinstance(value, bool):
            value = str(value).strip().lower() == "true"
        if field == "price":
            value = float(value)
        if field in ("name", "description", "category"):
            value = str(value).strip()
        values[field] = value
    return values


@app.get("/")
def home():
    name = request.args.get("name", "").strip()
    category = request.args.get("category", "").strip()
    available = request.args.get("available", "").strip()

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category.title())
    elif available in ("true", "false"):
        products = Product.find_by_availability(available == "true")
    else:
        products = Product.all()

    flash_message = "Success" if request.args.get("searched") == "1" else ""
    return render_template(
        "index.html",
        products=products,
        filters={"name": name, "category": category, "available": available},
        flash_message=flash_message,
    )


@app.post("/products")
def create_product():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json(silent=True) or {}
    required = ("name", "description", "category", "available", "price")
    if any(field not in data or data[field] in (None, "") for field in required):
        return jsonify({"error": "name, description, category, available and price are required"}), 400

    try:
        values = _product_values(data)
        product = Product(**values)
        product.save()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid product data"}), 400

    return jsonify(product.serialize()), 201


@app.get("/products")
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name.strip())
    elif category:
        products = Product.find_by_category(category.strip().title())
    elif available is not None and available.strip() != "":
        products = Product.find_by_availability(available.strip().lower() == "true")
    else:
        products = Product.all()

    return jsonify([product.serialize() for product in products]), 200


@app.get("/products/<int:product_id>")
def read_product(product_id):
    product = Product.find(product_id)
    if product:
        return jsonify(product.serialize()), 200
    return jsonify({"error": "Product not found"}), 404


@app.put("/products/<int:product_id>")
def update_product(product_id):
    product = Product.find(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json(silent=True) or {}
    try:
        for field, value in _product_values(data).items():
            setattr(product, field, value)
        product.save()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid product data"}), 400

    return jsonify(product.serialize()), 200


@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    # This project uses an idempotent DELETE response.
    return "", 204
