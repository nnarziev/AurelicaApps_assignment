from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=10)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
