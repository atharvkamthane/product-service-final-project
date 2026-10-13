"""Database model and query helpers for products."""
from service import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    price = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "available": bool(self.available),
            "price": float(self.price),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, product_id):
        return db.session.get(cls, product_id)

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def count(cls):
        return cls.query.count()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).order_by(cls.id).all()

    @classmethod
    def find_by_category(cls, category):
        category_value = category.strip().title()
        return cls.query.filter_by(category=category_value).order_by(cls.id).all()

    @classmethod
    def find_by_availability(cls, available):
        return cls.query.filter_by(available=bool(available)).order_by(cls.id).all()
