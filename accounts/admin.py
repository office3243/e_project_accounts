from django.contrib import admin
from .models import UserSession, User

admin.site.register(User)
admin.site.register(UserSession)
