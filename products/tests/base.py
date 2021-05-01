from rest_framework.test import APITestCase

from products.models import Product, Category


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

