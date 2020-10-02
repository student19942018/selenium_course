import pytest


def test_working_with_cart(app):
    app.fill_cart(count_products=3)
    app.clear_cart()
