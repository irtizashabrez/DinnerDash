from django.urls import reverse
from items.models import *
from authentications.models import MyUser
from django.test.client import RequestFactory
from test_plus.test import TestCase
from http import HTTPStatus
import pdb

class MyViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        user_pw = '12345()qW'
        user_admin = MyUser.object.create(
            full_name='admin',
            email='admin@admin.com',
            admin=True
        )
        user_admin.set_password(user_pw)
        user_admin.save()
        self.user_admin = user_admin
        user_b = MyUser.object.create(
            full_name='test user',
            email='test@test.com',
        )
        user_b.set_password(user_pw)
        user_b.save()
        self.user_b = user_b
        category = Category.objects.create(category='PakistaniTest 2')
        item = Item.objects.create(
            title='item test 1', description='this is test item',
            price=12, status='Available', photo='https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg',
        )
        item.category.add(category)

        self.item = item

    def test_user_exists(self):
        user_count = MyUser.object.all().count()
        self.assertEqual(user_count, 2)

    def test_admin_user(self):
        user_qs = MyUser.object.filter(email='admin@admin.com')
        user_a = user_qs.first()
        self.assertEqual(user_qs.count(), 1)
        self.assertTrue(user_a.is_admin)

    def test_normal_user(self):
        user_qs = MyUser.object.filter(email='test@test.com')
        user_a = user_qs.first()
        self.assertEqual(user_qs.count(), 1)
        self.assertFalse(user_a.is_admin)

    def test_add_category_admin(self):
        self.client.login(username=self.user_admin.email, password='12345()qW')
        response = self.client.get('/add-category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item_form.html')

    def test_add_category_user(self):
        self.client.login(username=self.user_b.email, password='12345()qW')
        response = self.client.get('/add-category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')

    def test_add_item_admin(self):
        self.client.login(username=self.user_admin.email, password='12345()qW')
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item_form.html')

    def test_add_item_user(self):
        self.client.login(username=self.user_b.email, password='12345()qW')
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')

    def test_update_item(self):
        response = self.client.get(reverse('update-item', args=['1']))
        self.assertEqual(response.status_code, 302)
        # noraml user
        self.client.login(username=self.user_b.email, password='12345()qW')
        response = self.client.get(reverse('update-item', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')

        # admin user
        self.client.login(username=self.user_admin.email, password='12345()qW')
        response = self.client.get(
            reverse('update-item', args=(self.item.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'items/item_form.html')

        url = reverse('update-item', args=(self.item.id,))
        category = Category.objects.create(category='new test category')
        data={
            'title': 'Item test 1',
            'description': 'this is test description',
            'price': 12,
            'status': 'Available',
            'photo': 'https://res.cloudinary.com/dweuirck0/image/upload/v1642502378/nmvg73wekwwfhcjidt6c.jpg',
            'category': [category]
        }
        response_v2 = self.client.post(url, kwargs=data)
        # pdb.set_trace()
        self.assertEqual(response_v2.status_code, HTTPStatus.OK)
# ................................................

    def test_item_delete(self):
        response = self.client.get(reverse('delete-item', args=['1']))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user_b.email, password='12345()qW')
        response = self.client.get(reverse('delete-item', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'error.html')

        self.client.login(username=self.user_admin.email,
                          password='123455()qW')
        response = self.client.post(
            reverse('delete-item', args=(self.item.id,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_item_view(self):
        response = self.client.get(reverse('item-detail', args=['1']))
        self.assertEqual(response.status_code, 200)

    def test_display_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_display_home_with_filter(self):
        response = self.client.get(reverse('home'), data={'q': 'sdf'})
        self.assertEqual(response.status_code, 200)
