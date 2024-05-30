from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.booking import Booking
from .tasks import send_email

@receiver(post_save, sender=Booking)
def booking_status_update(sender, instance, created, **kwargs):
    if created:
        send_email(instance.user.id, instance)
    else:
        send_email(instance.user.id, instance)



