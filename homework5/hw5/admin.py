from django.contrib import admin
from .models import Film, Seat, Order


class FilmAdmin(admin.ModelAdmin):
    list_display = ['title']

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number']

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_view_or_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(Film, FilmAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Order, OrderAdmin)
