from django.db import models
from django.core.validators import RegexValidator
from products.models import Product

_PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: "
            "'+111111111111'. Up to 15 digits allowed."
)


class Customer(models.Model):
    name = models.CharField(max_length=14, null=True)
    country = models.CharField(max_length=3, validators=[RegexValidator(
        regex='^.{3}$', message='Length has to be 3', code='nomatch'
    )], null=True)
    address = models.TextField()
    phone = models.CharField(verbose_name='phone',
                             validators=[_PHONE_REGEX],
                             max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders',
                                 on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)

    @property
    def total_cost(self):
        return sum(item.get_cost() for item in self.details.all())

    def __str__(self):
        return str(self.id)


class Detail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_details', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True)

    def get_cost(self):
        return self.product.price * self.quantity
