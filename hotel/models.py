from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Bookings(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
       singles = models.IntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(8)],default=0)
       doubles = models.IntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(16)],default=0)
       triples = models.IntegerField(validators=[MinValueValidator(0),
                                                 MaxValueValidator(8)],default=0)
       quadruples = models.IntegerField(validators=[MinValueValidator(0),
                                                    MaxValueValidator(4)],default=0)
       checkin_date = models.DateField(blank=False, auto_now=False, auto_now_add=False)
       checkout_date = models.DateField(blank=False, auto_now=False, auto_now_add=False)
       checkout_code = models.CharField(max_length=6, blank=False)
       amount = models.DecimalField(blank=False, max_digits=8, decimal_places=2)
       checkin = models.BooleanField(default=False)
       def __str__(self):
         return f"{self.user} - Quantity: {self.checkout_code} -  Rate: {self.amount}"


