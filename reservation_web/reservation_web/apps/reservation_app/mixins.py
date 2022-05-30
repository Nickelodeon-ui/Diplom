# pylint: skip-file

import imp
from django.views.generic.edit import FormMixin
from django.forms import ModelForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.base import ContextMixin

from .forms import Submit_BG_form


class SuggestionFormMixin(FormMixin):
    
    form_class = Submit_BG_form

    def post(self, request, *args, **kwargs):
        if request.POST.get("suggestion_bg"):
            form = Submit_BG_form(request.POST)
            if form.is_valid():
                # Отправка пожелания или отзыва менеджерам
                customer_name = form.cleaned_data["customer_name"]
                message = form.cleaned_data["message"]
                message = f"Имя: {customer_name} \nСообщение: {message}"
                send_mail(
                    "Поиск игры или отзыв покупателя",
                    message, 
                    settings.EMAIL_HOST_USER,  # В setting заменить на новый созданный
                    ["borodachnikolay@mail.ru"]  # Список менеджеров
                )
                return HttpResponseRedirect(self.request.get_full_path_info()) #Должно возвращать на ту же страницу но хз
