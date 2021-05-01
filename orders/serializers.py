from rest_framework import serializers

from .models import Order, Customer, Detail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'date')


class OrderWithTotalCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'date', 'total_cost')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'country', 'address', 'phone')


class OrderDetailsSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='order.customer')
    date = serializers.CharField(source='order.date')
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = Detail
        fields = ('order_id', 'customer', 'date', 'product_name', 'quantity')


class MakeOrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
