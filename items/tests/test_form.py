from test_plus.test import TestCase
from items.forms import ItemForm, CateoryForm
from items.models import Category
import pdb


class TestForm(TestCase):
    # set the

    def test_item_form_valid_data(self):
        category = Category.objects.create(category='PakistaniTest')
        data = {
            'title': 'Item test 1',
            'description': 'this is test description',
            'price': 12,
            'status': 'Available',
            'photo': 'https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg',
            'category': [category]
        }
        form = ItemForm(data)
        self.assertEqual(form.is_valid(), True)

    def test_item_form_negitiva_price(self):
        category = Category.objects.create(category='PakistaniTest')
        data = {
            'title': 'Item test 1',
            'description': 'this is test description',
            'price': -12,
            'status': 'Available',
            'photo': 'https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg',
            'category': [category]
        }
        form = ItemForm(data)
        self.assertEqual(form.is_valid(), False)

    def test_item_form_without_image(self):
        category = Category.objects.create(category='PakistaniTest')
        data = {
            'title': 'Item test 1',
            'description': 'this is test description',
            'price': 12,
            'status': 'Available',
            'category': [category]
        }
        form = ItemForm(data)
        self.assertEqual(form.is_valid(), True)

    def test_item_form_without_image(self):
        category = Category.objects.create(category='PakistaniTest')
        data = {
            'title': 'Item test 1',
            'description': 'this is test description',
            'price': 12,
            'status': 'Available',
            'category': [category]
        }
        form = ItemForm(data)
        self.assertEqual(form.is_valid(), True)

    def test_item_form_with_data(self):
        data = {}
        form = ItemForm(data)
        self.assertEqual(form.is_valid(), False)

    def test_category_form_valid_data(self):
        data = {
            'category': 'test category'
        }
        form = CateoryForm(data)
        self.assertEqual(form.is_valid(), True)

    def test_category_form_unvalid_data(self):
        data = {
            'category': 'test categorytest categorytest categorytest categorytest categorytest category'
        }
        form = CateoryForm(data)
        self.assertEqual(form.is_valid(), False)
