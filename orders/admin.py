from django.contrib import admin

from .models import Order, Detail, Customer


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'customer']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'order']
