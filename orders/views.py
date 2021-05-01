from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_200_OK

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from payments.models import Invoice
from products.models import Product
from .models import Order, Customer
import datetime
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import (
    OrderSerializer, CustomerSerializer, OrderWithTotalCostSerializer,
    OrderDetailsSerializer, MakeOrderSerializer)


@api_view()
def orders_without_details(request):
    orders = Order.objects.filter(details__isnull=True, date__lt=datetime.datetime(2016, 9, 6))
    if not orders:
        raise APIException("Not found orders")
    return Response(OrderSerializer(orders, many=True).data, status=HTTP_200_OK)


@api_view()
def customers_without_orders(request):
    customers = Customer.objects.exclude(orders__date__year=2016)
    if not customers:
        raise APIException("Not found customers")
    return Response(CustomerSerializer(customers, many=True).data, status=HTTP_200_OK)


@api_view()
def customers_last_orders(request):
    customers = Customer.objects.all()
    if not customers:
        raise APIException("Not found customers")
    result = []
    for customer in customers:
        if customer.orders:
            result.append({
                'id': customer.id,
                'name': customer.name,
                'last_order_date': customer.orders.order_by('date').last().date
            })
    return Response(result, status=HTTP_200_OK)


@api_view()
def orders_without_invoices(request):
    orders = Order.objects.filter(invoice__isnull=True)

    if not orders:
        raise APIException("Not found orders")
    return Response(OrderWithTotalCostSerializer(orders, many=True).data, status=HTTP_200_OK)


@api_view()
def number_of_products_in_year(request):
    countries = Customer.objects.all().values_list('country', flat=True).distinct()
    if not countries:
        raise APIException("No available countries")
    result = {}
    for country in countries:
        order_count = Order.objects.filter(date__year=2021, customer__country=country).count()
        if order_count > 0:
            result[country] = order_count

    return Response(result, status=HTTP_200_OK)


class OrdersView(APIView):

    def get(self, request: Request):
        order = Order.objects.filter(pk=request.query_params['order_id']).first()

        if not order:
            return Response({}, status=HTTP_200_OK)
        result = {
            'order_id': order.id,
            'date': order.date,
            'customer': order.customer.name,
            'order_details': []
        }
        for detail in order.details.all():
            result['order_details'].append({
                'product_name': detail.product.name,
                'quantity': detail.quantity
            })

        return Response(result, status=HTTP_200_OK)

    def post(self, request: Request):
        serializer = MakeOrderSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIException(serializer.errors)

        customer = Customer.objects.filter(pk=serializer.validated_data.get('customer_id')).first()
        if not customer:
            raise APIException(f'Not found customer with id={serializer.validated_data.get("customer_id")}')

        product = Product.objects.filter(pk=serializer.validated_data.get('product_id')).first()
        if not product:
            raise APIException(f'Not found product with id={serializer.validated_data.get("product_id")}')

        order = Order.objects.create(customer_id=customer.id, date=datetime.datetime.now())

        order.details.create(
            product_id=product.id,
            quantity=serializer.validated_data.get('quantity')
        )

        invoice = Invoice.objects.create(
            order_id=order.id,
            amount=order.total_cost,
            issued=datetime.datetime.now(),
            due=datetime.datetime.now() + datetime.timedelta(days=10)  # make due date after 10 days
        )

        if not invoice:
            return Response({'status': 'FAILED'})

        return Response({
            'status': 'SUCCESS',
            'invoice_number': invoice.id
        }, status=HTTP_200_OK)
