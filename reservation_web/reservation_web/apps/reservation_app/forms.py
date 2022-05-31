# pylint: skip-file

from audioop import add
import imp
import ipaddress
from lib2to3.pgen2.parse import ParseError
from tkinter import Widget
from attr import attrs
from django import forms
from django.test import RequestFactory
from psycopg2 import DatabaseError
from requests import request
from traitlets import default
from .models import Reservation, Property, Service, PROPERTY_TYPES_CHOICES, Image
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime
from address.forms import AddressField
from .contsts import DATE_FORMAT
from .utils import parse_address

class PropertyForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}),
        required=False,
    )

    type = forms.ChoiceField(
        widget=forms.Select(
            attrs={"style": "display: block"},
        ),
        choices=PROPERTY_TYPES_CHOICES,
        required=True,
    )

    address = AddressField()

    class Meta:
        model = Property
        fields = ["id", "name", "description", "type", "rooms_qty", "people_capacity", "price", "address"]


class SearchForReservationForm(forms.ModelForm):
    adults_qty = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={"min":"1", "step":"1", "max":"10"}))
    kids_qty = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={"min":"0", "step":"1", "max":"10"}))
    rooms_qty = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={"min":"1", "step":"1", "max":"10"}))
    
    address = AddressField()
    
    from_date = forms.DateField(
        widget=forms.DateInput(
            format=[DATE_FORMAT],
            attrs={"autocomplete": "off", "style": "width: 180px",}
        ),
        input_formats=[DATE_FORMAT],
        required=True,
        error_messages  = {'invalid': f'Пожалуйста введите дату заезда в формате день-месяц-год'}
    )
    to_date = forms.DateField(
        widget=forms.DateInput(
            format=[DATE_FORMAT],
            attrs={"autocomplete": "off", "style": "width: 180px",}
        ),
        input_formats=[DATE_FORMAT],
        required=True,
        error_messages  = {'invalid': f'Пожалуйста введите дату отъезда в формате день-месяц-год'}
    )
    
    budget_range = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for searched_service in Service.objects.filter(is_search_service=True):
             self.fields[
                 f'is_{searched_service.slug}_enabled'] = forms.BooleanField(
                    required=False,
                    help_text=searched_service.name,
                    initial=False,
                )

    def clean(self):
        self.check_dates()
        self.check_address()
        super().clean()
    
    def check_address(self):
        address_dict = parse_address(self.data)
        if not any(x for x in address_dict if address_dict[x]) or not address_dict["country"]:
            raise forms.ValidationError("К сожалению сервисы Google временно не отвечают. Пожалуйста расширьте поиск.")
        
        return None

    def check_dates(self):
        try:
            parsed_from_date = datetime.strptime(self.data["from_date"], DATE_FORMAT).date()
            parsed_to_date = datetime.strptime(self.data["to_date"], DATE_FORMAT).date()
        except Exception:
            return None

        if parsed_from_date < datetime.now().date():
            raise forms.ValidationError("Дата заезда не может быть раньше чем сегодняшняя дата")

        if parsed_to_date < datetime.now().date():
            raise forms.ValidationError("Дата отъезда не может быть раньше чем сегодняшняя дата")

        if parsed_from_date >= parsed_to_date:
            raise forms.ValidationError("Дата заезда не может быть позже чем дата отъезда или равняться ей")

        return None
    

    class Meta:
        model = Reservation
        fields = ["from_date", "to_date", "kids_qty", "adults_qty", "rooms_qty"]

    
class ReservePropertyForm(forms.ModelForm):
    adults_qty = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={"min":"1", "step":"1", "max":"10", "id": "adults_qty_id_2"}))
    kids_qty = forms.IntegerField(required=False, initial=0, widget=forms.NumberInput(attrs={"min":"0", "step":"1", "max":"10", "id": "kids_qty_id_2"}))
    rooms_qty = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={"min":"1", "step":"1", "max":"10", "id": "rooms_qty_id_2"}))

    from_date = forms.DateField(
        widget=forms.DateInput(
            format=[DATE_FORMAT],
            attrs={"autocomplete": "off", "style": "width: 180px; padding-left: 12px", 'placeholder': 'Прибытие', "id": "reserve_from_date_id"}
        ),
        input_formats=[DATE_FORMAT],
        required=True,
        error_messages  = {'invalid': f'Пожалуйста введите дату заезда в формате день-месяц-год'}
    )
    to_date = forms.DateField(
        widget=forms.DateInput(
            format=[DATE_FORMAT],
            attrs={"autocomplete": "off", "style": "width: 180px; padding-left: 12px", 'placeholder': 'Отъезд', "id": "reserve_to_date_id"}
        ),
        input_formats=[DATE_FORMAT],
        required=True,
        error_messages  = {'invalid': f'Пожалуйста введите дату отъезда в формате день-месяц-год'}
    )

    def clean(self):
        self.check_dates()
        super().clean()

    def check_dates(self):
        try:
            parsed_from_date = datetime.strptime(self.data["from_date"], DATE_FORMAT).date()
            parsed_to_date = datetime.strptime(self.data["to_date"], DATE_FORMAT).date()
        except Exception:
            return None

        if parsed_from_date < datetime.now().date():
            raise forms.ValidationError("Дата заезда не может быть раньше чем сегодняшняя дата")

        if parsed_to_date < datetime.now().date():
            raise forms.ValidationError("Дата отъезда не может быть раньше чем сегодняшняя дата")

        if parsed_from_date >= parsed_to_date:
            raise forms.ValidationError("Дата заезда не может быть позже чем дата отъезда или равняться ей")

        return None

    def save(self, request, property, commit=False):
        parsed_from_date = datetime.strptime(self.data["from_date"], DATE_FORMAT).date()
        parsed_to_date = datetime.strptime(self.data["to_date"], DATE_FORMAT).date()
        reservation = Reservation.objects.create(
            from_date=parsed_from_date, 
            to_date=parsed_to_date,
            kids_qty=self.data["kids_qty"],
            adults_qty=self.data["adults_qty"],
            resident_who_booked=getattr(request.user, "resident", None) or request.user.owner,
            booked_property=property,
            price_for_booking=(property.price * (parsed_to_date-parsed_from_date).days) + 10,
        )
        return reservation

    class Meta:
        model = Reservation
        fields = ["from_date", "to_date", "kids_qty", "adults_qty"]

class Submit_BG_form(forms.Form):
    customer_name = forms.CharField(required=False)
    message = forms.CharField(
        label="Ваше сообщение",
        widget=forms.Textarea,
        required=True
    )