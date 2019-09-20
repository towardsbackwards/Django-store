from django.test import TestCase
from django.test.client import Client
from mainapp.models import TrendyProduct, Product, Category
from authapp.models import ShopUser
from django.core.management import call_command


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db1.json')

        self.client = Client()

    def test_mainapp_urls(self):
        # главная без логина
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/products')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/products/0')
        self.assertEqual(response.status_code, 301)

        for category in Category.objects.all():
            response = self.client.get(f'/products/{category.pk}')
            self.assertEqual(response.status_code, 301)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
