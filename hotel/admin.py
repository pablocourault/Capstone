from django.contrib import admin
from .models import User, Room, Bookings

class RoomAdmin(admin.ModelAdmin):
    list_display = ("description","rate")

class BookingsAdmin(admin.ModelAdmin):
    list_display = ("user","singles","doubles","triples","quadruples","checkin_date","checkout_date","checkout_code","amount")


# Register your models here.

admin.site.register(User)
admin.site.register(Room, RoomAdmin)
admin.site.register(Bookings, BookingsAdmin)


