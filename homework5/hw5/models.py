from django.contrib.auth.models import User
from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    file = models.FileField(null=True, upload_to='uploads')
    trailer = models.CharField(max_length=1000)
    category = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.title


class Seat(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    # Add any other seat-related fields

    def __str__(self):
        return self.seat_number


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
