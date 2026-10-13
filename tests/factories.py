"""Factory Boy factory for fake Product records."""
import factory
from factory import fuzzy

from service.models import Product


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    category = fuzzy.FuzzyChoice(["Food", "Clothing", "Electronics", "Housewares"])
    available = fuzzy.FuzzyChoice([True, False])
    price = fuzzy.FuzzyDecimal(1.00, 1000.00, precision=2)
