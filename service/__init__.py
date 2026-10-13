"""Flask application setup for the Product Service."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import StaticPool

app = Flask(__name__, template_folder="templates")
app.config.update(
    TESTING=False,
    SQLALCHEMY_DATABASE_URI="sqlite://",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    },
)

db = SQLAlchemy(app)

# Import routes after app/db exist so the model can import db safely.
from service import routes  # noqa: E402,F401

with app.app_context():
    db.create_all()
