from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from .validators import phone_number_validator
from django.conf import settings
import requests
from django.shortcuts import redirect

api_key_2fa = settings.API_KEY_2FA


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('phone number'), max_length=13, validators=[phone_number_validator, ], unique=True)
    email = models.EmailField(_('email address'), blank=True)

    phone_verified = models.BooleanField(default=False)
    first_name = models.CharField(_('first name'), max_length=32, blank=True)
    last_name = models.CharField(_('last name'), max_length=32, blank=True)
    city = models.CharField(_('city'), max_length=30, blank=True, default="Pune")
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_first_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    @property
    def get_wallet(self):
        return self.wallet

    def otp_generate(self, request):
        hash_token = OtpSession.objects.create(user=self)
        request.session["otp_session_uuid"] = str(hash_token.uuid)
        url = "http://2factor.in/API/V1/{api_key}/SMS/{phone}/AUTOGEN/OTPSEND".format(api_key=api_key_2fa, phone=self.phone)
        response = requests.request("GET", url)
        data = response.json()
        request.session['otp_session_data'] = data['Details']
        return redirect("accounts:otp_verify")


class OtpSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return "{} - {}".format(self.user.__str__,
                                     self.uuid)
