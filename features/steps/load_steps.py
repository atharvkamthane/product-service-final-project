"""Step definitions for loading BDD background Product data."""
from behave import given


@given("the following products")
def step_impl(context):
    for row in context.table:
        data = {
            "name": row["name"],
            "description": row["description"],
            "category": row["category"],
            "available": row["available"].strip().lower() == "true",
            "price": float(row["price"]),
        }
        context.response = context.client.post("/products", json=data)
        assert context.response.status_code == 201, context.response.get_data(as_text=True)
