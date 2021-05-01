from datetime import datetime

from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from orders.models import Detail, Customer, Order
from products.models import Product
from products.tests.base import ApiBasesObjectsTest


class TestCategoriesView(ApiBasesObjectsTest):

    def test_get_categories(self) -> None:
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(len(response_msg), 2)
        self.assertEqual(response_msg[0], {'id': 1, 'name': 'Category 1'})
        self.assertEqual(response_msg[1], {'id': 2, 'name': 'Category 2'})


class TestProductCategoryView(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.req_data = {
            'product_id': 1
        }

    def test_get_product_category(self) -> None:
        response = self.client.get(reverse('product_category'), self.req_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg['name'], 'Category 1')

    def test_get_product_category_not_found_product(self) -> None:
        self.req_data['product_id'] = 1000
        response = self.client.get(reverse('product_category'), self.req_data)
        self.assertEqual(response.json()['detail'], f'Not found product with id='
                                                    f'{self.req_data["product_id"]}')


class TestProductsView(ApiBasesObjectsTest):

    def test_get_products(self) -> None:
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(len(response_msg), 3)
        pr1 = Product.objects.filter(pk=1).first()
        pr2 = Product.objects.filter(pk=2).first()
        pr3 = Product.objects.filter(pk=3).first()
        self.assertEqual(response_msg[0], {
            'id': pr1.id,
            'name': pr1.name,
            'category_id': pr1.category.id,
            'description': pr1.description,
            'price': str(pr1.price),
            'photo': pr1.photo
        })
        self.assertEqual(response_msg[1], {
            'id': pr2.id,
            'name': pr2.name,
            'category_id': pr2.category.id,
            'description': pr2.description,
            'price': str(pr2.price),
            'photo': pr2.photo
        })
        self.assertEqual(response_msg[2], {
            'id': pr3.id,
            'name': pr3.name,
            'category_id': pr3.category.id,
            'description': pr3.description,
            'price': str(pr3.price),
            'photo': pr3.photo
        })


class TestProductView(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.req_data = {
            'product_id': 1
        }

    def test_get_product(self) -> None:
        response = self.client.get(reverse('product_details'), self.req_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        pr = Product.objects.filter(pk=self.req_data['product_id']).first()
        self.assertEqual(response_msg['id'], pr.id)
        self.assertEqual(response_msg['name'], pr.name)
        self.assertEqual(response_msg['category_id'], pr.category_id)
        self.assertEqual(response_msg['description'], pr.description)
        self.assertEqual(response_msg['price'], str(pr.price))
        self.assertEqual(response_msg['photo'], pr.photo)

    def test_get_product_not_found(self) -> None:
        self.req_data['product_id'] = 1000
        response = self.client.get(reverse('product_details'), self.req_data)
        self.assertEqual(response.json()['detail'], f'Not found product with id='
                                                    f'{self.req_data["product_id"]}')


class TestHighDemandProductsMethod(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.total_orders_pr1 = 12
        self.total_orders_pr2 = 15
        self.customer = Customer.objects.create(
            name='John',
            country='Uzb',
            address='some address',
            phone='+998999999999'
        )
        self.order = Order.objects.create(
            customer=self.customer,
            date=datetime.now()
        )
        for _ in range(self.total_orders_pr1):
            Detail.objects.create(
                order=self.order,
                product=self.product_1,
                quantity=20
            )
        for _ in range(self.total_orders_pr2):
            Detail.objects.create(
                order=self.order,
                product=self.product_2,
                quantity=20
            )

    def test_get_products(self) -> None:
        response = self.client.get(reverse('high_demand_products'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg[0], {
            'id': 1,
            'name': 'product 1',
            'total_orders': self.total_orders_pr1
        })
        self.assertEqual(response_msg[1], {
            'id': 2,
            'name': 'product 2',
            'total_orders': self.total_orders_pr2
        })
