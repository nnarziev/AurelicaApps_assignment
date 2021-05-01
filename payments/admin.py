from django.contrib import admin

from .models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'issued', 'due']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['time', 'amount', 'invoice']
