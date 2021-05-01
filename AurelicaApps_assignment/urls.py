from django.contrib import admin
from django.urls import path, include

from payments import views as payment_views
from orders import views as order_views
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('expired_invoices', payment_views.expired_invoices,
         name='expired_invoices'),
    path('wrong_date_invoices', payment_views.wrong_date_invoices,
         name='wrong_date_invoices'),
    path('overpaid_invoices', payment_views.overpaid_invoices,
         name='overpaid_invoices'),
    path('orders_without_details', order_views.orders_without_details,
         name='orders_without_details'),
    path('customers_without_orders', order_views.customers_without_orders,
         name='customers_without_orders'),
    path('customers_last_orders', order_views.customers_last_orders,
         name='customers_last_orders'),
    path('high_demand_products', product_views.high_demand_products,
         name='high_demand_products'),
    path('bulk_products', product_views.bulk_products,
         name='bulk_products'),
    path('number_of_products_in_year', order_views.number_of_products_in_year,
         name='number_of_products_in_year'),
    path('orders_without_invoices', order_views.orders_without_invoices,
         name='orders_without_invoices'),
    path('order/', include('orders.urls')),
    path('payment/', include('payments.urls')),
]
