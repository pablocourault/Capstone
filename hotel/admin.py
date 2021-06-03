from django.contrib import admin
from .models import User, Room, Bookings, Guests, Consumptions, Services, Comments, Messages

class RoomAdmin(admin.ModelAdmin):
    list_display = ("description","rate")

class BookingsAdmin(admin.ModelAdmin):
    list_display = ("user","singles","doubles","triples","quadruples","checkin_date","checkout_date","checkout_code","amount","checkin")


# Register your models here.

admin.site.register(User)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bookings, BookingsAdmin)
admin.site.register(Services)

# Registered models for developement purposes
admin.site.register(Guests)
admin.site.register(Consumptions)
admin.site.register(Comments)
admin.site.register(Messages)


