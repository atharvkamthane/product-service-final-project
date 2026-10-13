# Product Service Final Project

A Flask CRUD API for managing products, accompanied by model tests, route tests, and Behave BDD scenarios with Selenium.

## Project structure

- `service/models.py` — Product model and query helpers
- `service/routes.py` — Product REST API and home/search page
- `service/templates/index.html` — Search UI used by browser tests
- `tests/factories.py` — Factory Boy ProductFactory
- `tests/test_models.py` — model CRUD and search tests
- `tests/test_routes.py` — API route tests
- `features/steps/load_steps.py` — background product data loader
- `features/products.feature` — seven BDD scenarios
- `features/steps/web_steps.py` — Selenium/Behave step definitions

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Behave browser scenarios also require Chrome/Chromium and a compatible ChromeDriver.
