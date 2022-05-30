from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView, View
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse,FileResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail

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
                Resident.objects.create()
                Owner.objects.create()
                # Для предотвращения ошибки получаем созданный объект из БД, потому что пока что у нас в user лежит объект
                # без поля One to one (которое задастся путем сигнала-ресивера), а просто объект класса user - для доступа к полям address и phone
                address = form.cleaned_data["address"]
                phone = form.cleaned_data["phone"]
                email = form.cleaned_data["email"]

                send_mail(
                    "Уведомление интернет-магазина",
                    "Уведомление, что вы успешно зарегистрировались в интернет-магазине настольных игр", 
                    settings.EMAIL_HOST_USER,  # В setting заменить на новый созданный
                    [email]  # Список менеджеров
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