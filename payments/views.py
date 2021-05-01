from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from .models import Invoice, Payment
from datetime import datetime
from rest_framework.status import HTTP_200_OK
from django.db.models import F
from django.db.models import Sum

from .serializers import InvoiceSerializer, WrongInvoiceSerializer, PaymentSerializer, InvoiceIdSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view


@api_view()
def expired_invoices(request):
    invoices = Invoice.objects.filter(due__lt=datetime.now().date(), due__isnull=False)
    if not invoices:
        return Response([], status=HTTP_200_OK)
    return Response(InvoiceSerializer(invoices, many=True).data, status=HTTP_200_OK)


@api_view()
def wrong_date_invoices(request):
    invoices = Invoice.objects.filter(order__date__gt=F('issued'))
    if not invoices:
        return Response([], status=HTTP_200_OK)
    return Response(WrongInvoiceSerializer(invoices, many=True).data, status=HTTP_200_OK)


@api_view()
def overpaid_invoices(request):
    invoices = Invoice.objects.annotate(total_price=Sum('payments__amount')) \
        .filter(total_price__gt=F('amount'))
    result = []
    for invoice in invoices:
        result.append({
            'invoice_id': invoice.id,
            'reimbursement_amount': invoice.total_price - invoice.amount
        })

    return Response(result)


class PaymentsView(APIView):

    def get(self, request: Request):
        payment = Payment.objects.filter(pk=request.query_params['id']).first()

        if not payment:
            raise APIException(f"Not found payment with id="
                               f"{request.query_params['id']}")

        return Response(PaymentSerializer(payment, many=False).data, status=HTTP_200_OK)

    def post(self, request: Request):
        serializer = InvoiceIdSerializer(data=request.data)
        if not serializer.is_valid():
            raise APIException(serializer.errors)

        invoice = Invoice.objects.filter(pk=serializer.validated_data.get('invoice_id')).first()
        if not invoice:
            raise APIException(f"Not found invoice with id="
                               f"{serializer.validated_data.get('invoice_id')}")

        payment = invoice.payments.create(
            invoice_id=serializer.validated_data.get('invoice_id'),
            time=datetime.now().time(),
            amount=invoice.amount  # full amount of invoice because amount for payment was not specified
        )

        if not payment:
            return Response({'status': 'FAILED'})

        return Response({
            'payment_status': 'SUCCESS',
            'payment_details': PaymentSerializer(payment, many=False).data
        }, status=HTTP_200_OK)
