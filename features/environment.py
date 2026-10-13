"""Behave environment hooks for the browser-based Product Service tests."""
from threading import Thread

from selenium import webdriver
from werkzeug.serving import make_server

from service import app, db
from service.models import Product


def before_all(context):
    context.base_url = "http://127.0.0.1:5000"
    context.client = app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

    context.server = make_server("127.0.0.1", 5000, app)
    context.server_thread = Thread(target=context.server.serve_forever, daemon=True)
    context.server_thread.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.browser = webdriver.Chrome(options=options)


def before_scenario(context, scenario):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    context.copied_product_id = None
    context.api_response = None
    context.flash_message = None


def after_all(context):
    browser = getattr(context, "browser", None)
    if browser is not None:
        browser.quit()
    server = getattr(context, "server", None)
    if server is not None:
        server.shutdown()
