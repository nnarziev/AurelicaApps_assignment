from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_200_OK

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Product, Category
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import CategorySerializer, BulkProductSerializer, ProductSerializer
from django.db.models import Count


@api_view()
def high_demand_products(request):
    products = Product.objects.annotate(total_orders=Count('order_details__id')).filter(total_orders__gt=10)
    result = []
    for product in products:
        result.append({
            'id': product.id,
            'name': product.name,
            'total_orders': product.total_orders
        })

    return Response(result, status=HTTP_200_OK)


@api_view()
def bulk_products(request):
    products = Product.objects.filter(order_details__quantity__gte=8)
    if not products:
        raise APIException("Not found products")

    return Response(BulkProductSerializer(products, many=True).data, status=HTTP_200_OK)


class CategoriesView(APIView):

    def get(self, request: Request):
        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data, status=HTTP_200_OK)


class ProductCategoryView(APIView):

    def get(self, request: Request):
        product = Product.objects.filter(pk=request.query_params['product_id']).first()
        if not product:
            raise APIException(f"Not found product with id="
                               f"{request.query_params['product_id']}")

        return Response(CategorySerializer(product.category, many=False).data, status=HTTP_200_OK)


class ProductsView(APIView):

    def get(self, request: Request):
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True).data, status=HTTP_200_OK)


class ProductView(APIView):

    def get(self, request: Request):
        product = Product.objects.filter(pk=request.query_params['product_id']).first()
        if not product:
            raise APIException(f"Not found product with id="
                               f"{request.query_params['product_id']}")

        return Response(ProductSerializer(product, many=False).data, status=HTTP_200_OK)
