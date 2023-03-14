from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import uuid


class User(AbstractUser):
    pass
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # makes more readable items in admin panel
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    numbers = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = not bool(self.pk)
        super().save(*args, **kwargs)
        if created:
            arrival = Arrival(product=self, quantity=self.numbers, store=self.store)
            arrival.save()

    def delete(self, *args, **kwargs):
        arrival = Arrival.objects.filter(product=self).first()
        if arrival:
            arrival.delete()
        super().delete(*args, **kwargs)


class Expense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} ({self.sender} -> {self.receiver})'


class Arrival(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name}"


@receiver(post_save, sender=Product)
def create_arrival_on_product_create(sender, instance, created, **kwargs):
    if created:
        arrival = Arrival(product=instance, quantity=instance.numbers, store=instance.store)
        arrival.save()


@receiver(post_delete, sender=Product)
def delete_arrival_on_product_delete(sender, instance, **kwargs):
    Arrival.objects.filter(product=instance).delete()

