from rest_framework import serializers

from .models import Invoice, Payment


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'order_id', 'amount', 'issued', 'due')


class WrongInvoiceSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')
    order_date = serializers.CharField(source='order.date')

    class Meta:
        model = Invoice
        fields = ('id', 'issued', 'order_id', 'order_date')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'invoice_id', 'time', 'amount')


class InvoiceIdSerializer(serializers.Serializer):
    invoice_id = serializers.IntegerField()
