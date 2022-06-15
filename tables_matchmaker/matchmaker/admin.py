from django.contrib import admin

from .models import Room, Player


# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Room", {'fields': ['id', 'game']}),
    ]


admin.site.register(Room, RoomAdmin)
admin.site.register(Player)
