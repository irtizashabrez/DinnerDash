from django.test import SimpleTestCase
from django.urls import reverse, resolve
from items.views import *


class testUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('home')
        check = resolve(url).func.view_class
        self.assertEquals(check, DisplayItems)

    def test_create_url(self):
        url = reverse('create-item')
        check = resolve(url).func.view_class
        self.assertEquals(check, AddItem)

    def test_update_url(self):
        url = reverse('update-item', args=['18'])
        check = resolve(url).func.view_class
        self.assertEquals(check, UpdateItem)

    def test_add_category_url(self):
        url = reverse('add-category')
        check = resolve(url).func.view_class
        self.assertEquals(check, AddCategory)

    def test_item_url(self):
        url = reverse('item-detail', args=['1'])
        check = resolve(url).func.view_class
        self.assertEquals(check, ItemView)

    def test_delete_url(self):
        url = reverse('delete-item', args=['1'])
        check = resolve(url).func.view_class
        self.assertEquals(check, DeleteItem)
