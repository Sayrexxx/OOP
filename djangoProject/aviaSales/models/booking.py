from django.db import models

from .user import MyUser
from .flight import Flight


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(MyUser, related_name='bookings', on_delete=models.CASCADE)
    number = models.AutoField(primary_key=True)
    amount = models.PositiveSmallIntegerField(default=1)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
            
    STATUS_CHOICES = (
        ("В обработке ", "В обработке"),
        ("Принят", "Принят"),
        ("Отменён", "Отменён"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Принят")