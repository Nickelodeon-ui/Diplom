from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Resident(User):
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    profile_picture = models.ImageField(upload_to="residents_images/", null=True)

    class Meta:
        verbose_name  = "residents"
        verbose_name_plural = "residents"

    def __str__(self):
        return f"Это постоялец {self.username}: {self.first_name} {self.last_name}"


class Owner(User):
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    profile_picture = models.ImageField(upload_to="owners_images/", null=True)

    class Meta:
        verbose_name  = "owners"
        verbose_name_plural = "owners"

    def __str__(self):
        return f"Это арендодатель {self.username}: {self.first_name} {self.last_name}"
