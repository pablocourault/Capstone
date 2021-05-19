from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
       def __str__(self):
        return f"{self.username}"

class Guests(models.Model):
       guest = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
       def __str__(self):
        return f"{self.guest}"

class Room(models.Model):
       description = models.CharField(max_length=64, blank=False)
       roomtype = models.CharField(max_length=1, blank=False)
       quantity = models.IntegerField()
       rate = models.DecimalField(blank=False, max_digits=4, decimal_places=2)
       def __str__(self):
         return f"{self.description} - Quantity: {self.quantity} -  Rate: {self.rate}"

