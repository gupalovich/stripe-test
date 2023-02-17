import json

from django.test import TestCase

from shop.products.tests.factories import Item, ItemFactory

from ..services import (
    convert_currency_symbol_to_stripe_type,
    convert_price_by_currency,
    convert_price_to_cents,
    get_selected_currency,
)


class ServicesTests(TestCase):
    def setUp(self):
        pass

    def test_get_selected_currency(self):
        body = json.dumps({"currency": Item.Currency.RUB})
        result = get_selected_currency(body)
        self.assertEqual(result, Item.Currency.RUB)

    def test_get_selected_currency_blank(self):
        body = json.dumps({})
        result = get_selected_currency(body)
        self.assertFalse(result)

    def test_convert_currency_symbol_to_stripe_type_rub(self):
        result = convert_currency_symbol_to_stripe_type(Item.Currency.RUB)
        self.assertEqual(result, "rub")

    def test_convert_currency_symbol_to_stripe_type_usd(self):
        result = convert_currency_symbol_to_stripe_type(Item.Currency.USD)
        self.assertEqual(result, "usd")

    def test_convert_currency_symbol_to_stripe_type_unknown(self):
        result = convert_currency_symbol_to_stripe_type("123")
        self.assertEqual(result, "rub")

    def test_convert_price_by_currency_rub(self):
        item = ItemFactory(currency=Item.Currency.RUB)
        result = convert_price_by_currency(Item.Currency.RUB, item.price, item.currency)
        self.assertEqual(result, item.price)

    def test_convert_price_by_currency_usd_to_rub(self):
        item = ItemFactory(currency=Item.Currency.USD)
        result = convert_price_by_currency(Item.Currency.RUB, item.price, item.currency)
        self.assertEqual(result, item.price * 70)

    def test_convert_price_by_currency_rub_to_usd(self):
        item = ItemFactory(currency=Item.Currency.RUB)
        result = convert_price_by_currency(Item.Currency.USD, item.price, item.currency)
        self.assertEqual(result, item.price / 70)

    def test_convert_price_by_currency_unknown(self):
        item = ItemFactory(currency=Item.Currency.RUB)
        result = convert_price_by_currency("123", item.price, item.currency)
        self.assertEqual(result, item.price)

    def test_convert_price_to_cents(self):
        item = ItemFactory(currency=Item.Currency.RUB)
        self.assertEqual(int(item.price * 100), convert_price_to_cents(item.price))
