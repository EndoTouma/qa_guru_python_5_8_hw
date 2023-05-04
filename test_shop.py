import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(0)
        assert product.quantity == 1000
        product.buy(285)
        assert product.quantity == 715
        product.buy(715)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            assert product.buy(1001)


class TestCart:

    def test_add_product(self, cart, product):
        assert len(cart.products) == 0
        cart.add_product(product)
        assert cart.products[product] == 1
        cart.add_product(product, 10)
        assert cart.products[product] == 11
        assert len(cart.products) == 1

    def test_remove_product(self, cart, product):
        cart.add_product(product, 234)
        cart.remove_product(product, 44)
        assert cart.products[product] == 190
        cart.remove_product(product)
        assert len(cart.products) == 0
        cart.add_product(product, 456)
        cart.remove_product(product, 890)
        assert len(cart.products) == 0
        cart.add_product(product, 899)
        cart.remove_product(product, 899)
        assert len(cart.products) == 0, 'Удаление продукта из корзины полностью'

    def test_clear(self,  cart, product):
        cart.add_product(product, 34)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 56)
        assert cart.get_total_price() == 5600

    def test_buy_product(self, cart, product):
        cart.add_product(product, 56)
        cart.buy()
        assert len(cart.products) == 0

    def test_product_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            assert cart.buy()
