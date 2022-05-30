from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm


class OwnerOrResidentForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.TextInput(
            attrs={
                "class": "form_input",
                "placeholder": "E-mail"
                }
            )
        )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form_input",
                "placeholder": "Телефон"
                }
            )
        )

    password1 = forms.CharField(
        label=("Пароль:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                "class": "form_input",
                "placeholder": "Пароль"
                }
            )
        )

    password2 = forms.CharField(
        label=("Подтверждение пароля:"),
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                "class": "form_input",
                "placeholder": "Повторите пароль"
            }
        ),
        strip=False
    )

    user_type = forms.ChoiceField(
        choices=(
            ("resident", "Аредатор"),
            ("owner", "Арендодатель"),
        )
    )


    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + \
            ("email", "first_name", "last_name",
             "phone", "password1", "password2", "user_type")
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Пользовательское имя",
                "class": "form_input"}
            ),
            "first_name": forms.TextInput(attrs={
                "placeholder": "Имя",
                "class": "form_input"}
            ),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Фамилия",
                "class": "form_input"}
            ),
        }


class MyLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
                               'autofocus': True, "placeholder": "Пользовательское имя", "class": "form_input"})
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', "placeholder": "Пароль", "class": "form_input"}),
    )
