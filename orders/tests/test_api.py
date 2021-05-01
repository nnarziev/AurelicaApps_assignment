from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from orders.models import Detail
from orders.tests.base import ApiBasesObjectsTest


class TestOrdersView(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.order_detail = Detail.objects.create(
            order=self.order,
            product=self.product_1,
            quantity=10
        )

        self.req_data_get = {
            'order_id': self.order.id
        }

        self.req_data_post = {
            'customer_id': self.customer.id,
            'product_id': self.product_2.id,
            'quantity': 100
        }

    def test_get_order_details_by_id(self) -> None:
        response = self.client.get(reverse('order_details'), self.req_data_get)
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg['order_id'], self.order.id)
        self.assertEqual(response_msg['customer'], self.order.customer.name)
        self.assertEqual(response_msg['order_details'][0], {
            'product_name': self.order_detail.product.name,
            'quantity': self.order_detail.quantity
        })

    def test_make_order(self) -> None:
        response = self.client.post(reverse('make_order'), self.req_data_post, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'SUCCESS')

    def test_make_order_not_found_product(self) -> None:
        self.req_data_post['product_id'] = 1000
        response = self.client.post(reverse('make_order'), self.req_data_post, format='json')
        self.assertEqual(response.json()['detail'], f'Not found product with id='
                                                    f'{self.req_data_post["product_id"]}')

    def test_make_order_not_found_customer(self) -> None:
        self.req_data_post['customer_id'] = 1000
        response = self.client.post(reverse('make_order'), self.req_data_post, format='json')
        self.assertEqual(response.json()['detail'], f'Not found customer with id='
                                                    f'{self.req_data_post["customer_id"]}')
