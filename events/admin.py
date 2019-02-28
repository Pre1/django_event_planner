from django.contrib import admin
from .models import Booking, Event, Follow

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(Follow)


