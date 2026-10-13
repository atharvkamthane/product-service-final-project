"""Unit tests for Product model CRUD and search behavior."""
import unittest

from service import app, db
from service.models import Product
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.session.remove()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_read_product(self):
        product = ProductFactory()
        product.save()

        assert product.id is not None
        found = Product.find(product.id)

        assert found.id == product.id
        assert found.name == product.name
        assert found.description == product.description
        assert found.price == product.price

    def test_update_product(self):
        product = ProductFactory()
        product.save()
        original_id = product.id

        product.name = "Updated Product"
        product.description = "testing"
        product.save()

        found = Product.find(original_id)
        assert found.id == original_id
        assert found.name == "Updated Product"
        assert found.description == "testing"

    def test_delete_product(self):
        product = ProductFactory()
        product.save()

        assert Product.count() == 1
        product.delete()
        assert Product.count() == 0

    def test_list_all_products(self):
        assert Product.count() == 0

        for _ in range(5):
            ProductFactory().save()

        products = Product.all()
        assert len(products) == 5

    def test_find_by_name(self):
        for _ in range(5):
            ProductFactory(name="Laptop").save()

        results = Product.find_by_name("Laptop")
        assert len(results) == 5
        for product in results:
            assert product.name == "Laptop"

    def test_find_by_category(self):
        for _ in range(10):
            ProductFactory(category="Electronics").save()

        results = Product.find_by_category("Electronics")
        assert len(results) == 10
        for product in results:
            assert product.category == "Electronics"

    def test_find_by_availability(self):
        for _ in range(10):
            ProductFactory(available=True).save()

        results = Product.find_by_availability(True)
        assert len(results) == 10
        for product in results:
            assert product.available is True


if __name__ == "__main__":
    unittest.main()
