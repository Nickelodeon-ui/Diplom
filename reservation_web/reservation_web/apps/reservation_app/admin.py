# pylint: skip-file

from django.contrib import admin

from .models import Property, Reservation, Image, Service


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image


class ReservationInline(admin.StackedInline):
    model = Reservation
    

class ServiceInline(admin.TabularInline):
    model = Service.properties.through


class PropertyAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
        ReservationInline,
        ServiceInline,
    ]


admin.site.register(Property, PropertyAdmin)

admin.site.register(Reservation)

admin.site.register(Service)
