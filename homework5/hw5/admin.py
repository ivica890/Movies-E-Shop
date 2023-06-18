from django.contrib import admin
from .models import Film, Seat, Order


class FilmAdmin(admin.ModelAdmin):
    list_display = ['title']


class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(Film, FilmAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Order, OrderAdmin)
