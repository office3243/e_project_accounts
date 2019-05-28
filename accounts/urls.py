from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import CustomLoginForm


app_name = "accounts"

urlpatterns = [
    url(r"^register/$", views.RegisterView.as_view(), name='register'),
    url(r"^otp_verify/$", views.otp_verify, name='otp_verify'),

    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomLoginForm),
        name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    #
    # url(r'^otp_input/$', views.otp_input, name='otp_input')

]
