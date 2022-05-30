from django.urls import path

from .views import (
    RegistrationFormView,
    MyLogoutView,
    MyLoginView,
)

urlpatterns = [
    path("register", RegistrationFormView.as_view(), name="register"),
    path("login", MyLoginView.as_view(), name="login"),
    path("logout", MyLogoutView.as_view(), name="logout"),
]
