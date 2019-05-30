from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import CustomLoginForm
from django.views.generic import TemplateView


app_name = "accounts"

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='accounts/home.html'), name="home"),

    url(r"^register/$", views.RegisterView.as_view(), name='register'),
    url(r"^otp/resend/$", views.otp_resend, name='otp_resend'),

    url(r"^otp/verify/$", views.OTPVerifyView.as_view(), name='otp_verify'),

    url(r"^password/change/$", views.password_change, name='password_change'),

    url(r"^password/reset/$", views.PasswordResetView.as_view(), name='password_reset'),

    url(r"^password/reset/new/$", views.PasswordResetNewView.as_view(), name='password_reset_new'),
    url(r"^password/reset/otp/resend/$", views.password_reset_otp_resend, name='password_reset_otp_resend'),

    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomLoginForm),
        name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    #
    # url(r'^otp_input/$', views.otp_input, name='otp_input')

]
