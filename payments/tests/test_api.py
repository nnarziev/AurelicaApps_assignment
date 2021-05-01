import datetime

from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from payments.models import Payment, Invoice
from payments.tests.base import ApiBasesObjectsTest


class TestPaymentsView(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.invoice = Invoice.objects.create(
            order=self.order,
            amount=1000,
            issued=datetime.datetime.now(),
            due=datetime.datetime.now() + datetime.timedelta(days=10)
        )
        self.payment = Payment.objects.create(
            invoice=self.invoice,
            time=datetime.datetime.now().time(),
            amount=100
        )

        self.req_data_get = {
            'id': self.payment.id
        }

        self.req_data_post = {
            'invoice_id': self.invoice.id
        }

    def test_get_payment_by_id(self) -> None:
        response = self.client.get(reverse('payment_details'), self.req_data_get)
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg, {
            'id': self.payment.id,
            'invoice_id': self.invoice.id,
            'time': str(self.payment.time),
            'amount': "{:.2f}".format((self.payment.amount))
        })

    def test_get_payment_not_found(self) -> None:
        self.req_data_get['id'] = 1000
        response = self.client.get(reverse('payment_details'), self.req_data_get)
        self.assertEqual(response.json()['detail'], f'Not found payment with id='
                                                    f'{self.req_data_get["id"]}')

    def test_make_payment(self) -> None:
        response = self.client.post(reverse('make_payment'), self.req_data_post, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['payment_status'], 'SUCCESS')

    def test_make_payment_not_found(self) -> None:
        self.req_data_post['invoice_id'] = 1000
        response = self.client.post(reverse('make_payment'), self.req_data_post, format='json')
        self.assertEqual(response.json()['detail'], f'Not found invoice with id='
                                                    f'{self.req_data_post["invoice_id"]}')


class TestOverPaidInvoicesMethod(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.invoice_1 = Invoice.objects.create(
            order=self.order,
            amount=1000,
            issued=datetime.datetime.now(),
            due=datetime.datetime.now() + datetime.timedelta(days=10)
        )
        self.invoice_2 = Invoice.objects.create(
            order=self.order_1,
            amount=500,
            issued=datetime.datetime.now(),
            due=datetime.datetime.now() + datetime.timedelta(days=10)
        )
        self.payment_1 = Payment.objects.create(
            invoice=self.invoice_1,
            time=datetime.datetime.now().time(),
            amount=900
        )
        self.payment_2 = Payment.objects.create(
            invoice=self.invoice_1,
            time=datetime.datetime.now().time(),
            amount=300
        )
        self.payment_3 = Payment.objects.create(
            invoice=self.invoice_2,
            time=datetime.datetime.now().time(),
            amount=200
        )
        self.payment_4 = Payment.objects.create(
            invoice=self.invoice_2,
            time=datetime.datetime.now().time(),
            amount=400
        )

    def test_get_overpaid_invoices(self) -> None:
        response = self.client.get(reverse('overpaid_invoices'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg[0], {
            'invoice_id': self.invoice_1.id,
            'reimbursement_amount': self.payment_1.amount + self.payment_2.amount - self.invoice_1.amount
        })
        self.assertEqual(response_msg[1], {
            'invoice_id': self.invoice_2.id,
            'reimbursement_amount': self.payment_3.amount + self.payment_4.amount - self.invoice_2.amount
        })


class TestWrongDateInvoicesMethod(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.invoice_1 = Invoice.objects.create(
            order=self.order,
            amount=1000,
            issued=datetime.datetime.now() - datetime.timedelta(days=10),
            due=datetime.datetime.now() + datetime.timedelta(days=10)
        )
        self.invoice_2 = Invoice.objects.create(
            order=self.order_1,
            amount=500,
            issued=datetime.datetime.now() - datetime.timedelta(days=10),
            due=datetime.datetime.now() + datetime.timedelta(days=10)
        )

    def test_get_wrong_date_invoices(self) -> None:
        response = self.client.get(reverse('wrong_date_invoices'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg[0]['id'], self.invoice_1.id)
        self.assertEqual(response_msg[0]['order_id'], self.invoice_1.order_id)
        self.assertEqual(response_msg[1]['id'], self.invoice_2.id)
        self.assertEqual(response_msg[1]['order_id'], self.invoice_2.order_id)


class TestExpiredInvoicesMethod(ApiBasesObjectsTest):

    def setUp(self) -> None:
        self.invoice_1 = Invoice.objects.create(
            order=self.order,
            amount=1000,
            issued=datetime.datetime.now(),
            due=datetime.datetime.now() - datetime.timedelta(days=10)
        )
        self.invoice_2 = Invoice.objects.create(
            order=self.order_1,
            amount=500,
            issued=datetime.datetime.now(),
            due=datetime.datetime.now() - datetime.timedelta(days=10)
        )

    def test_get_expired_invoices(self) -> None:
        response = self.client.get(reverse('expired_invoices'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        response_msg = response.json()
        self.assertEqual(response_msg[0]['id'], self.invoice_1.id)
        self.assertEqual(response_msg[0]['order_id'], self.invoice_1.order_id)
        self.assertEqual(response_msg[0]['amount'], "{:.2f}".format((self.invoice_1.amount)))

        self.assertEqual(response_msg[1]['id'], self.invoice_2.id)
        self.assertEqual(response_msg[1]['order_id'], self.invoice_2.order_id)
        self.assertEqual(response_msg[1]['amount'], "{:.2f}".format((self.invoice_2.amount)))
