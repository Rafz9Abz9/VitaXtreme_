from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email address"), unique=True, null=False)
    first_name = models.CharField(
        _("first name"), max_length=50, blank=True, null=True)
    last_name = models.CharField(
        _("last name"), max_length=50, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_subscribed_newsletter = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(
        _("email address"), unique=True, null=True, default="")
    phone = models.TextField(max_length=20, null=True, default="")
    street_address = models.TextField(max_length=250, null=True, default="")
    post_code = models.TextField(
        max_length=20, blank=True, null=True, default="")
    city = models.TextField(max_length=80, null=True, default="")
    state = models.TextField(max_length=80, default="")
    country = models.CharField(max_length=200,  null=True, choices=CountryField(
    ).choices + [('', 'Select Country')])

    def __str__(self):
        return f'Shipping Address for {self.user}'

    class Meta:
        verbose_name_plural = "ShippingAddress"
