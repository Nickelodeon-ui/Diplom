from ast import Add
import imp
from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView, View
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail
from datetime import datetime

from reservation_app.models import Image, Property
from reservation_app.forms import Submit_BG_form, PropertyForm
from .models import Resident, Owner
from .forms import OwnerOrResidentForm, MyLoginForm


class RegistrationFormView(FormView):

    form_class = OwnerOrResidentForm
    template_name = "login_registration_app/registration.html"
    success_url = reverse_lazy("reservation_app:properties_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Если пользователь уже есть в БД
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                import ipdb
                ipdb.set_trace()
                
                user = form.save()
                
                data_for_creation = {
                    "user": user,
                    "phone": form.cleaned_data["phone"],
                }

                Resident.objects.create(**data_for_creation) if form.cleaned_data["user_type"] == "resident" else Owner.objects.create(**data_for_creation)
                
                send_mail(
                    "Уведомление от сайта по аренде жилых помещений",
                    "Уведомление, что вы успешно зарегистрировались на сайте по аренде жилых помещений!", 
                    settings.EMAIL_HOST_USER,  # В setting заменить на новый созданный
                    [form.cleaned_data["email"]]  # Список менеджеров
                )

                login(request, user)
                return HttpResponseRedirect(self.get_success_url())
        else:
            # return HttpResponseRedirect(self.request.path_info)
            return render(request, "login_registration_app/registration.html", {"form": form})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("reservation_app:properties_list")


class MyLoginView(LoginView):
    authentication_form = MyLoginForm
    template_name = "login_registration_app/login.html"

    def get_success_url(self):
        return reverse_lazy("reservation_app:properties_list")


class MyProfileView(View):
    owner_profile_template = "login_registration_app/owner/index.html"
    resident_profile_template = "login_registration_app/resident/index.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        template_to_render = self.owner_profile_template if getattr(user, "owner", None) else self.resident_profile_template
        context = self.get_owner_profile_context(user) if getattr(user, "owner", None) else self.get_resident_profile_context(user)
        return render(request, template_to_render, context=context)

    def get_owner_profile_context(self, user):
        context = {}
        owner = user.owner

        # import ipdb
        # ipdb.set_trace()

        context["managed_properties"] = owner.properties.all()
        context["review_form"] = Submit_BG_form()
        context["booked_properties"] = owner.properties.filter(reservations__from_date__lte=datetime.now().date()).distinct()
        return context

    def get_resident_profile_context(self, user):
        context = {}
        return context

class AddPropertyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login_registration_app/owner/add-room.html", self.get_context(request))

    def post(self, request, *args, **kwargs):
        form = PropertyForm(request.POST)

        if form.is_valid():
            new_property = form.save()
            new_property.owner = request.user.owner
            new_property.save()

            for image in request.FILES.getlist("images"):
                Image.objects.create(source=new_property, image=image)
        
        return HttpResponseRedirect(reverse_lazy("login_registration_app:user_profile"))

    def get_context(self, request):
        context = {}
        owner = request.user.owner
        context["managed_properties"] = owner.properties.all()
        context["review_form"] = Submit_BG_form()
        context["booked_properties"] = owner.properties.filter(reservations__from_date__lte=datetime.now().date()).distinct()
        context["property_form"] = PropertyForm()
        context["review_form"] = Submit_BG_form()
        return context


class DeletePropertyView(View):
    def get(lf, request, *args, **kwargs):
        Property.objects.get(id=kwargs["pk"]).delete()
        return HttpResponseRedirect(reverse_lazy("login_registration_app:user_profile")) 


class UpdatePropertyView(View):
    def get(self, request, *args, **kwargs):
        property_from_db = Property.objects.get(id=kwargs["pk"])
        form = PropertyForm(instance=property_from_db)
        return render(
            request,
            "login_registration_app/owner/add-room.html",
            self.get_context(request, form, property_from_db.id)
        )

    def post(self, request, *args, **kwargs):
        existing_property = Property.objects.get(id=kwargs["pk"])
        form = PropertyForm(request.POST, instance=existing_property)

        if form.is_valid():
            updated_instance = form.save()
            updated_instance.images.all().delete()
            for image in request.FILES.getlist("images"):
                Image.objects.create(source=updated_instance, image=image)
        
        return HttpResponseRedirect(reverse_lazy("login_registration_app:user_profile"))

    def get_context(self, request, form, prop_id):
        context = {}
        owner = request.user.owner
        context["managed_properties"] = owner.properties.all()
        context["review_form"] = Submit_BG_form()
        context["booked_properties"] = owner.properties.filter(reservations__from_date__lte=datetime.now().date()).distinct()
        context["property_form"] = form
        context["review_form"] = Submit_BG_form()
        context["property_id"] = prop_id
        return context
