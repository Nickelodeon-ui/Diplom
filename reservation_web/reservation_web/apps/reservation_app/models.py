# pylint: skip-file

from datetime import datetime
from operator import mod
from secrets import choice
from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.urls import reverse
from address.models import AddressField
from .contsts import DATE_FORMAT

from login_registration_app.models import Owner, Resident


PROPERTY_TYPES_CHOICES = (
    ("HOTEL", "Отель"),
    ("APARTMENT", "Квартира"),
    ("HOUSE", "Дом"),
    ("HOSTEL", "Хостел"),
    ("COTTAGE", "Коттедж"),
)


class Property(models.Model):
    name = models.CharField('Название жилого помещения', max_length=50)
    description = models.TextField(
        'Описание жилого помещения', null=True, blank=True)
    type = models.CharField("Тип жилого помещения",
                            choices=PROPERTY_TYPES_CHOICES, max_length=15)
    rooms_qty = models.PositiveIntegerField("Количество комнат/номеров")
    people_capacity = models.PositiveIntegerField(
        "Вместимость жилого помещения (человек)")
    price = models.PositiveIntegerField("Цена за день проживания")
    add_date = models.DateField("Дата добавления", default=timezone.now())
    rating = models.FloatField(
        "Оценка жилого помещения", null=True, blank=True)
    owner = models.ForeignKey(
        Owner, related_name="properties", on_delete=models.CASCADE)
    # address = models.ForeignKey(Address, related_name="property", on_delete=models.SET_NULL, null=True)
    address = AddressField(on_delete=models.CASCADE)

    @property
    def full_address(self):
        return self.address.raw

    class Meta:
        verbose_name = "properties"
        verbose_name_plural = "properties"

    def __str__(self):
        return self.name

    @property
    def is_reserved(self):
        return True if self.reservations.objects.filter(from_date__gte=datetime.now()) else False

    # def get_absolute_url(self):
    #     return reverse("boardgames:one_bg", kwargs={"slug": str(self.slug)})


class Image(models.Model):
    source = models.ForeignKey(
        Property, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images/")


class Service(models.Model):
    """
    Удобства: wifi и тд
    """
    slug = models.SlugField(
        "Уникальный идентификатор удобсва", unique=True, db_index=True)
    img = models.ImageField("Иконка", upload_to="facility_icons/")
    name = models.CharField("Название удобсва", max_length=15)
    is_search_service = models.BooleanField("Удобство используется при поиске?", default=False)
    properties = models.ManyToManyField(
        Property, verbose_name="Помещение с удобством", related_name="services", null=True, blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    kids_qty = models.PositiveIntegerField("Количество детей")
    adults_qty = models.PositiveIntegerField("Количество взрослых")
    resident_who_booked = models.ForeignKey(
        Resident, verbose_name="Человек, который забронировал помещение", related_name="reservations", on_delete=models.CASCADE)
    booked_property = models.ForeignKey(
        Property, verbose_name="Забронированное помещение", related_name="reservations", on_delete=models.CASCADE)
