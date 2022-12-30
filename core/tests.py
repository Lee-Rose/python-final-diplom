from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from rest_framework import generics, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.models import Product
from core.serializers import ProductSerializer
from core.views import ProductsView

User = get_user_model()

class TestListProductsView(TestCase):
    def setUp(self):
        self.endpoint_url = '/api/products/'
        self.client = APIClient()


    def test_route_resolves_to_correct_view(self):
        found = resolve(self.endpoint_url)
        self.assertEqual(found.func.view_class, ProductsView)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_gets_200_products_list(self):

        product_1 = Product.objects.create(
            name='product_1',
            model='product_1',
            price_rrc=Decimal('200.00'),
        )
        product_2 = Product.objects.create(
            name='product_2',
            model='product_2',
            price_rrc=Decimal('300.00'),
        )

        expected_data = {
            product_1.id: {
                'id': product_1.id,
                'name': product_1.name,
                'model': product_1.model,
                'price_rrc': str(product_1.price_rrc),
                'categories': list(product_1.categories.values_list('name', flat=True)),
            },
            product_2.id: {
                'id': product_2.id,
                'name': product_2.name,
                'model': product_2.model,
                'price_rrc': str(product_2.price_rrc),
                'categories': list(product_2.categories.values_list('name', flat=True)),
            },
        }
        user = User.objects.create(username='john.doe')
        self.client.force_login(user)
        response = self.client.get(self.endpoint_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = {p['id']: p for p in response.json()}
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data, expected_data)


class TestProductSerializer(TestCase):
    def test_all_data(self):
        product = Product.objects.create(name='iPhone', model='177281', price_rrc=Decimal('89000.00'))
        serializer = ProductSerializer(product)

        self.assertEqual(set(serializer.data.keys()), {'id', 'name', 'model', 'categories', 'price_rrc'})
        self.assertEqual(serializer.data['id'], product.id)
        self.assertEqual(serializer.data['name'], product.name)
        self.assertEqual(serializer.data['model'], product.model)
        self.assertEqual(set(serializer.data['categories']), set(product.categories.values_list('name', flat=True)))
        self.assertEqual(len(serializer.data['categories']), len(product.categories.values_list('name', flat=True)))
        self.assertEqual(serializer.data['price_rrc'], str(product.price_rrc))



