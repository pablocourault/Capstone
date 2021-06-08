from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class User(AbstractUser):
       def __str__(self):
        return f"{self.username}"


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


class Guests(models.Model):
       guest = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
       booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, blank=False)
       def __str__(self):
        return f"Usuario: {self.guest} - Booking: {self.booking}"


class Services(models.Model):
       description = models.CharField(max_length=64, blank=False)
       description_es = models.CharField(max_length=64, blank=False)
       description_pt = models.CharField(max_length=64, blank=False)
       message = models.CharField(max_length=512, blank=False, default='Service request received')
       message_es = models.CharField(max_length=512, blank=False, default='Solicitud recibida')
       message_pt = models.CharField(max_length=512, blank=False, default='Pedido recebido')
       rate = models.DecimalField(blank=False, max_digits=6, decimal_places=2)
       def __str__(self):
        return f"Service: {self.description} - Rate: {self.rate}"


class Consumptions(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
       booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, blank=False)
       service = models.ForeignKey(Services, on_delete=models.DO_NOTHING, blank=False)
       date = models.DateField(blank=False, auto_now=False, auto_now_add=False)
       quantity = models.IntegerField(validators=[MinValueValidator(1),
                                                  MaxValueValidator(5)],default=1)
       amount = models.DecimalField(blank=False, max_digits=6, decimal_places=2)
       def __str__(self):
        return f"Usuario: {self.user} - Booking: {self.booking.checkout_code} - Description: {self.service.description} - Date: {self.date} - Amount: {self.amount}"       


class Comments(models.Model):
       user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False)
       date = models.DateField(blank=False, auto_now=False, auto_now_add=False)
       comment = models.CharField(max_length=512, blank=False)
       score = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(10)],default=0)
       def __str__(self):
        return f"Usuario: {self.user} - Date: {self.date} - Comment: {self.comment}"


class Messages(models.Model):
       user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='user_from',)
       date = models.DateField(blank=False, auto_now=False, auto_now_add=False)
       addressee = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='user_to',)
       message = models.CharField(max_length=512, blank=False)
       state = models.CharField(max_length=1, blank=False)
       def __str__(self):
        return f"From: {self.user} - Date: {self.date} - To: {self.addressee} - Message: {self.message}"









