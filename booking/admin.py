from django.contrib import admin

from booking.models import Session, SessionSlot

# Register your models here.
admin.site.register(Session)
admin.site.register(SessionSlot)