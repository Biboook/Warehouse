from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Store(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # makes more readable items in admin panel
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    numbers = models.PositiveIntegerField(default=0)
    # price = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} ({self.sender} -> {self.receiver})'

