from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrdersView.as_view(), name="make_order"),
    path('details', views.OrdersView.as_view(), name='order_details'),
]
