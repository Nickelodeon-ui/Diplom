from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resident")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    profile_picture = models.ImageField(upload_to="residents_images/", null=True)

    class Meta:
        verbose_name  = "residents"
        verbose_name_plural = "residents"

    def __str__(self):
        return f"Это постоялец {self.user.username}: {self.user.first_name} {self.user.last_name}"


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owner")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    profile_picture = models.ImageField(upload_to="owners_images/", null=True)

    class Meta:
        verbose_name  = "owners"
        verbose_name_plural = "owners"

    def __str__(self):
        return f"Это арендодатель {self.user.username}: {self.user.first_name} {self.user.last_name}"
