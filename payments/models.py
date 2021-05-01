from django.db import models
from orders.models import Order


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    issued = models.DateTimeField()
    due = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    time = models.TimeField(null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
