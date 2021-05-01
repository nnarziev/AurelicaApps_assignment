from django.urls import path

from . import views

urlpatterns = [
    path('', views.PaymentsView.as_view(), name="make_payment"),
    path('details', views.PaymentsView.as_view(), name='payment_details'),
]
