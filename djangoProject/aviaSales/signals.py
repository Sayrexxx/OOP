from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models.booking import Booking
from .tasks import send_email

@receiver(post_save, sender=Booking)
def booking_saved(sender, instance, created, **kwargs):
    send_email(instance.user.id, instance)

@receiver(post_delete, sender=Booking)
def booking_deleted(sender, instance, **kwargs):
    send_email(instance.user.id, instance, message=f'Booking {instance.number} was deleted by administrator. Contact us for additional information')
