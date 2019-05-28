from django.contrib import admin
from .models import OtpSession, User

admin.site.register(User)
admin.site.register(OtpSession)
