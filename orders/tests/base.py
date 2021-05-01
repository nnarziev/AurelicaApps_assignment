from rest_framework.test import APITestCase

from payments.models import Payment, Invoice
from orders.models import Order, Detail, Customer
from datetime import datetime

from products.models import Category, Product


class ApiBasesObjectsTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category_1 = Category.objects.create(name='Category 1')
        cls.category_2 = Category.objects.create(name='Category 2')

        cls.product_1 = Product.objects.create(
            name='product 1',
            category=cls.category_1,
            description='description of product 1',
            price=100,
            photo='photo url 1'
        )
        cls.product_2 = Product.objects.create(
            name='product 2',
            category=cls.category_1,
            description='description of product 2',
            price=200,
            photo='photo url 2'
        )
        cls.product_3 = Product.objects.create(
            name='product 3',
            category=cls.category_2,
            description='description of product 3',
            price=300,
            photo='photo url 3'
        )
        cls.customer = Customer.objects.create(
            name='John',
            country='Uzb',
            address='some address',
            phone='+998999999999'
        )
        cls.order = Order.objects.create(
            customer=cls.customer,
            date=datetime.now()
        )
        cls.order_1 = Order.objects.create(
            customer=cls.customer,
            date=datetime.now()
        )