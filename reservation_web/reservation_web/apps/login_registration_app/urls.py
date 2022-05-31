from django.urls import path

from .views import (
    RegistrationFormView,
    MyLogoutView,
    MyLoginView,
    MyProfileView,
    AddPropertyView,
    DeletePropertyView,
    UpdatePropertyView,
)

urlpatterns = [
    path("register", RegistrationFormView.as_view(), name="register"),
    path("login", MyLoginView.as_view(), name="login"),
    path("logout", MyLogoutView.as_view(), name="logout"),
    path('my-profile', MyProfileView.as_view(), name="user_profile"),
    path('add-property', AddPropertyView.as_view(), name="add_property"),
    path('delete-property/<int:pk>', DeletePropertyView.as_view(), name="delete_property"),
    path('update-property/<int:pk>', UpdatePropertyView.as_view(), name="update_property"),
]
