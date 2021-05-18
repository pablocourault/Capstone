from django.contrib import admin
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    list_display =("description","rate")
# Register your models here.

admin.site.register(Room, RoomAdmin)

