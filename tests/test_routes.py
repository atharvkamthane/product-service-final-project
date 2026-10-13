"""Route tests for the Product Service REST API."""
import unittest

from service import app, db
from service.models import Product
from tests.factories import ProductFactory


class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_read_product(self):
        product = ProductFactory()
        product.save()

        response = self.client.get(f"/products/{product.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == product.name

    def test_update_product(self):
        product = ProductFactory()
        response = self.client.post("/products", json=product.serialize())
        assert response.status_code == 201

        created = response.get_json()
        product_id = created["id"]
        response = self.client.put(
            f"/products/{product_id}",
            json={"description": "unknown"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["description"] == "unknown"

    def test_delete_product(self):
        product = ProductFactory()
        product.save()
        count_before = Product.count()

        response = self.client.delete(f"/products/{product.id}")
        assert response.status_code == 204
        assert response.data == b""

        response = self.client.get(f"/products/{product.id}")
        assert response.status_code == 404
        assert Product.count() == count_before - 1

    def test_list_all_products(self):
        for _ in range(5):
            ProductFactory().save()

        response = self.client.get("/products")
        assert response.status_code == 200
        assert len(response.get_json()) == 5

    def test_list_by_name(self):
        for _ in range(3):
            ProductFactory(name="Laptop").save()
        ProductFactory(name="Phone").save()
        ProductFactory(name="Tablet").save()

        response = self.client.get("/products?name=Laptop")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        for product in data:
            assert product["name"] == "Laptop"

    def test_list_by_category(self):
        for _ in range(3):
            ProductFactory(category="Electronics").save()
        ProductFactory(category="Furniture").save()
        ProductFactory(category="Clothing").save()

        response = self.client.get("/products?category=Electronics")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        for product in data:
            assert product["category"] == "Electronics"

    def test_list_by_availability(self):
        for _ in range(3):
            ProductFactory(available=True).save()
        ProductFactory(available=False).save()
        ProductFactory(available=False).save()

        response = self.client.get("/products?available=true")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
        for product in data:
            assert product["available"] is True


if __name__ == "__main__":
    unittest.main()
