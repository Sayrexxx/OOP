from django.contrib import admin

from .models.user import MyUser
from .models.flight import Flight
from .models.booking import Booking
from .models.notification import Notification



admin.site.register(MyUser)
admin.site.register(Flight)
admin.site.register(Booking)
admin.site.register(Notification)