import imp
from django.test import TestCase
from items.models import Item
import pytest

# @pytest.mark.skip to skip test case

# def test_example():
#     assert 1 == 1


@pytest.mark.django_db
def test_new_item(item_factory):
    # print(item_factory.photo)
    assert item_factory.price > 0


# @pytest.mark.parametrize(
#     "title, category, description, price, status, validity",
#     [
#         ("NewTitle", "test category", "NewDescription", "123", "OK", True),
#         # ("NewTitle 2", "test category", "NewDescription", "-123", "OK", False),
#     ],
# )
# def test_product_instance(
#     db, product_factory, title, category, description, price, status, validity
# ):
#     test = product_factory(
#         title=title,
#         category=category,
#         description=description,
#         price=price,
#         status=status,
#         # validity=validity
#     )
#     item = Item.objects.all().count
#     assert item == validity
