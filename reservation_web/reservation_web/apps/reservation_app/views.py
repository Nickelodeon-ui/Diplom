# pylint: skip-file
import folium
import os
import csv
import io
from pathlib import Path
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from django.views.generic import ListView, DetailView, FormView, View
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse_lazy, reverse
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from django.db.models import Q
from reservation_web.apps.reservation_app.contsts import DATE_FORMAT
import json

from reservation_web.apps.reservation_app.utils import parse_address

from .models import Property, Reservation, Service
from .forms import Submit_BG_form, SearchForReservationForm, ReservePropertyForm
from .mixins import SuggestionFormMixin
from .utils import parse_address
from django.db.models import Max


class PropertiesListView(SuggestionFormMixin, ListView):

    model = Property
    template_name = "home.html"
    context_object_name = "properties"

    def dispatch(self, request, *args, **kwargs):
        if "max_searched_properites" in request.session.keys():
            request.session.pop("max_searched_properites")
        if "searched_val" in request.session.keys():
            request.session.pop("searched_val")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForReservationForm()
        context["review_form"] = Submit_BG_form()
        context["max_properties"] = self.model.objects.count()
        return context

    def get_queryset(self):
        return self.model.objects.all()[:9]


class MorePropertiesView(View):
    def get(self, request, *args, **kwargs):
        properties = Property.objects.values_list()

        lower_border = kwargs["lower_border"]
        upper_border = lower_border + 3

        reached_max = True if upper_border >= len(properties) else False

        properties = properties[lower_border:upper_border]
        return JsonResponse(data={"data": properties, "reached_max": reached_max})


class MoreSearchedPropertiesView(View):
    def get(self, request, *args, **kwargs):
        max_searched_properites = request.session.get("max_searched_properites")
        searched_val = request.session.get("searched_val")
        properties = Property.objects.filter(
            name__contains=searched_val).values_list()

        lower_border = kwargs["lower_border"]
        upper_border = lower_border + 3

        reached_max = True if upper_border >= max_searched_properites else False

        properties = properties[lower_border:upper_border]
        return JsonResponse(data={"data": properties, "reached_max": reached_max})


class BookPropertyView(View):
    pass


class SearchForReservationView(View):
    def post(self, request, *args, **kwargs):
        
        form = self.initiate_data(request)
        
        print("VIEW")
        print(self.initial_data)

        if not form.is_valid():
            return self.handling_invalid_form(request, form)

        suitable_properties_qs = self.search_properties_by_criterias()
        recommended_properties_qs = self.get_recommened_properties_1()
        # recommended_properties_qs = self.get_recommened_properties_2()

        context = {
            "properties": suitable_properties_qs,
            "recommended_properties": recommended_properties_qs,
            "max_properties": suitable_properties_qs.count(),
            "review_form": SuggestionFormMixin.form_class(),
            }
        return render(request, "home.html", context=context)

    def initiate_data(self, request):
        """
        For filters we need:
        wanted_people_capacity, wanted_rooms_qty, min_price, max_price,
        country -> town -> street, search_services_slugs, from_date, to_date
        """
        self.initial_data = request.POST

        # Form
        self.form = SearchForReservationForm(self.initial_data)
        self.form_data = self.form.data

        # Dates
        self.from_date = self.form_data["from_date"]
        self.to_date = self.form_data["to_date"]

        # Additional info
        self.wanted_people_capacity = int(self.form_data["kids_qty"]) + int(self.form_data["adults_qty"])
        self.wanted_rooms_qty = int(self.form_data["rooms_qty"])

        # Budget
        budget_range_str = self.initial_data["budget_range"]
        self.min_price = int(budget_range_str.split()[1].strip())
        self.max_price = int(budget_range_str.split()[-1].strip())

        # Address 
        self.address_dict = parse_address(self.initial_data)
        self.country = self.address_dict["country"]
        self.town = self.address_dict["town"]
        self.street = self.address_dict["street"]

        # Services
        self.search_services_slugs = [key[3:-8] for key in self.form_data if key.startswith("is")]

        return self.form

    def handling_invalid_form(self, request, form):
        context={}
        context["search_form"] = form
        context["review_form"] = Submit_BG_form()
        context["max_properties"] = Property.objects.count()
        context["properties"] = Property.objects.all()[:9]
        return render(request, "home.html", context)

    def search_properties_by_criterias(self):
        suitable_properties_qs = Property.objects.filter(address__locality__state__country__name=self.country)

        if self.town:
            suitable_properties_qs = suitable_properties_qs.filter(address__locality__name=self.town)
        if self.street:
            suitable_properties_qs = suitable_properties_qs.filter(address__route=self.street)

        suitable_properties_qs = suitable_properties_qs.filter(
            people_capacity__gte=self.wanted_people_capacity,
            rooms_qty__gte=self.wanted_rooms_qty,
            price__range=[self.min_price, self.max_price],
        ).exclude(
            Q(reservations__from_date__range=[self.from_date, self.to_date])
            |
            Q(reservations__to_date__range=[self.from_date, self.to_date])
        )

        if self.search_services_slugs:
            for search_service_slug in self.search_services_slugs:
                suitable_properties_qs = suitable_properties_qs.filter(services__slug=search_service_slug)

        self.suitable_properties = suitable_properties_qs.distinct()
        return self.suitable_properties

    def get_recommened_properties_1(self):
        recommended_properties_qs = Property.objects.filter(
            address__locality__state__country__name=self.country,
            people_capacity__gte=self.wanted_people_capacity,
        ).exclude(
            Q(reservations__from_date__range=[self.from_date, self.to_date])
            |
            Q(reservations__to_date__range=[self.from_date, self.to_date])
        )
        
        if self.town:
            recommended_properties_qs = recommended_properties_qs.filter(address__locality__name=self.town)

        max_price_from_db = recommended_properties_qs.aggregate(price=Max("price"))["price"]
        max_rooms_qty_from_db = recommended_properties_qs.aggregate(rooms=Max("rooms_qty"))["rooms"]

        # Evaluate each property by the distance to the input data from user 
        # https://www.edureka.co/blog/k-nearest-neighbors-algorithm/ (step 2)
        for property in recommended_properties_qs:
            property.rate = self._rate_property(property, max_price_from_db, max_rooms_qty_from_db)

        recommended_properties_list = list(recommended_properties_qs)
        sorted_recommended_list = sorted(recommended_properties_list, key=lambda x: x.rate)
        sorted_recommended_set = set(sorted_recommended_list[:3])
        
        # import ipdb
        # ipdb.set_trace()

        suitable_properties_set = set(self.suitable_properties)
        return sorted_recommended_set - suitable_properties_set

    def _rate_property(self, property, max_price_from_db, max_rooms_qty_from_db):
        distance = 0

        if property.price > self.max_price:
            distance += pow((property.price - self.max_price)/max_price_from_db, 2)

        distance += pow((property.rooms_qty - self.wanted_rooms_qty)/max_rooms_qty_from_db, 2)
        distance += 0.5 * (len(self.search_services_slugs) - property.services.filter(slug__in=self.search_services_slugs).count())
        return distance


    def get_recommened_properties_2(self):
        pass


class PropertyDetailView(SuggestionFormMixin, DetailView):
    model = Property
    context_object_name = "property"
    template_name = "reservation_app/property_detail.html"
    
    def handling_invalid_form(self, request, form):
        context={}
        context["search_form"] = SearchForReservationForm()
        context["review_form"] = Submit_BG_form()
        context["reservation_form"] = form
        context["property"] = self.get_object()
        context["booked_ranges"] = json.dumps(
            [[from_d.strftime("%m-%d-%Y"), to_d.strftime("%m-%d-%Y")] for from_d, to_d in self.get_object().reservations.values_list("from_date", "to_date")]
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("VIEW")
        print(request.POST)
        
        form = ReservePropertyForm(request.POST)

        if not form.is_valid():
            return self.handling_invalid_form(request, form)

        import ipdb
        ipdb.set_trace()
        # Посмотреть как получать человека который бронирует

        form.save(request, self.get_object())

        context = {
            "property": self.get_object(),
            "search_form": SearchForReservationForm(),
            "review_form": Submit_BG_form(),
            "reservation_form": ReservePropertyForm(),
            "is_booking_completed": True,
            }
        return reverse(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # import ipdb
        # ipdb.set_trace()

        context["booked_ranges"] = json.dumps(
            [[from_d.strftime("%m-%d-%Y"), to_d.strftime("%m-%d-%Y")] for from_d, to_d in self.get_object().reservations.values_list("from_date", "to_date")]
        )
        print(context["booked_ranges"])
        context["search_form"] = SearchForReservationForm()
        context["reservation_form"] = ReservePropertyForm()
        context["review_form"] = Submit_BG_form()
        return context


# class DownloadCSVView(View):
#     def get(self, request, *args, **kwargs):
#         bg_qs = BoardGame.objects.get_queryset_with_url()

#         with open("bg_catalog.csv", 'w', newline='', encoding='utf-8') as csvfile:
#             fieldnames = ["Название на русском", "Название на английском",
#                 "Количество на складе", "Цена", "Ссылка"]
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#             for bg in bg_qs:
#                 writer.writerow({"Название на русском": bg.get('name'), "Название на английском": bg.get('eng_name'),
#                                 "Количество на складе": bg.get('quantity'), "Цена": bg.get('price'), "Ссылка": 'http://127.0.0.1:8000' + bg.get('url')})

#         with open("bg_catalog.csv", 'r', newline='', encoding='utf-8') as csvfile:
#             response = HttpResponse(csvfile, content_type="text/csv")
#             response['Content-Disposition'] = 'attachment; filename="bg_catalog.csv"'

#         os.remove('bg_catalog.csv')
#         return response


# class DownloadPDFView(View):

#     def get(self, request, *args, **kwargs):
#         pdfmetrics.registerFont(TTFont('CustomFont', Path(
#             str(settings.PROJECT_ROOT) + "/static/boardgames/fonts/Vera.ttf")))
#         custom_p_style = ParagraphStyle(
#             'Custom_p_style', fontName='CustomFont', fontSize=11)

#         qs = BoardGame.objects.get_queryset_with_url()
#         buffer = io.BytesIO()

#         doc = SimpleDocTemplate(buffer, rightMargin=0,
#                                 leftMargin=0, topMargin=0, bottomMargin=0)

#         elements = []
#         data = [
#             [
#             Paragraph(bg.get('name'), custom_p_style),
#             bg.get('quantity'),
#             bg.get('price'),
#             'http://127.0.0.1:8000' + bg.get('url')
#             ]
#             for bg in qs]
#         data.insert(0, [
#             Paragraph("Название на русском", custom_p_style),
#             Paragraph("Количество на складе", custom_p_style),
#             "Цена",
#             "Ссылка"
#             ])

#         t = Table(data, colWidths=[150, 55, 60, 300],
#                   rowHeights=55, splitByRow=True)
#         t.setStyle(
#             TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.pink),
#                 ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
#                 ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
#                 ('FONT', (0, 0), (-1, -1), 'CustomFont', 11)
#             ])
#         )
#         elements.append(t)
#         doc.build(elements)

#         buffer.seek(0)
#         return FileResponse(buffer, as_attachment=True, filename='bg_catalog.pdf')


class AboutUsView(SuggestionFormMixin, View):
    def get(self, request, *args, **kwargs):
        m = folium.Map(location=[53.907260, 27.439810], zoom_start=15)
        style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
        style_rivers = {'color': 'blue'}
        folium.Marker(
        [53.907260, 27.439810], popup='<i>Офис организации "Твоя столица"</i>'
    ).add_to(m)
        m=m._repr_html_()
        context = {
            "form": self.get_form(),
            "map": m
        }
        return render(request, "reservation_app/about_us.html", context)
