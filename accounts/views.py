import requests
from .models import UserSession
from .forms import RegisterForm, PasswordResetForm, PasswordResetNewForm
from django.views.generic import TemplateView, ListView, FormView
from django.http import Http404, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


USER_MODEL = get_user_model()
api_key = settings.API_KEY_2FA


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "accounts/register.html"

    def form_valid(self, form):
        new_user = form.save()
        return new_user.otp_generate(self.request)


def otp_verify(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        url = "http://2factor.in/API/V1/{0}/SMS/VERIFY/{1}/{2}".format(api_key, request.session['user_session_data'], user_otp)
        response = requests.request("GET", url)
        data = response.json()
        user_session = UserSession.objects.get(uuid=request.session["user_session_uuid"])
        user = user_session.user
        if data['Status'] == "Success":
            user.is_active = True
            user.phone_verified = True
            user.save()
            del request.session['user_session_uuid']
            del request.session['user_session_data']
            user_session.delete()
            return HttpResponse("Sucess Verified {}".format(user.phone))
        else:
            messages.warning(request, "please enter correct OTP!")
            return render(request, "accounts/otp_verify.html")
    else:
        return render(request, "accounts/otp_verify.html")


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {
        'form': form
    })


class PasswordResetView(FormView):

    template_name = "accounts/password_reset.html"
    form_class = PasswordResetForm

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone')
        try:
            user = USER_MODEL.objects.get(phone=phone)
            return user.password_reset_otp_generate(self.request)
        except USER_MODEL.DoesNotExist:
            messages.warning(self.request, "Phone number not registered.")
            return redirect("accounts:password_reset")


class PasswordResetNewView(FormView):

    template_name = "accounts/password_reset_new.html"
    form_class = PasswordResetNewForm

    def form_valid(self, form):
        otp = form.cleaned_data.get('otp')
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        user_session = UserSession.objects.get(uuid=self.request.session["user_session_uuid"])
        user = user_session.user

        url = "http://2factor.in/API/V1/{0}/SMS/VERIFY/{1}/{2}".format(api_key,
                                                                       self.request.session['user_session_data'], otp)
        response = requests.request("GET", url)
        data = response.json()
        if data['Status'] == "Success":
            user.set_password(password1)
            user.save()
            del self.request.session['user_session_uuid']
            del self.request.session['user_session_data']
            user_session.delete()
            messages.success(self.request, "Password changed")
            return redirect("accounts:home")
        else:
            messages.warning(self.request, "please enter correct OTP!")
            return redirect("accounts:password_reset_new")


#
# def otp_input(request):
#     if request.method == "POST":
#         user_otp = request.POST['otp']
#         url = "http://2factor.in/API/V1/{0}/SMS/VERIFY/{1}/{2}".format(api_key, request.session['user_session_data'], user_otp)
#         response = requests.request("GET", url)
#         data = response.json()
#         user_session = UserSession.objects.get(uuid=request.session["user_session_uuid"])
#         user = user_session.user
#         if data['Status'] == "Success":
#             user.is_active = True
#             user.save()
#             del request.session['user_session_uuid']
#             del request.session['user_session_data']
#             user_session.delete()
#             return HttpResponse("Sucess Verified {}".format(user.username))
#         else:
#             messages.warning(request, "please enter correct OTP!")
#     return render(request, "accounts/otp_input.html")
#
#
#
#
#
#
# def register(request):
#     form = UserCreationForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             phone = request.POST['phone']
#             url = "http://2factor.in/API/V1/{api_key}/SMS/{phone}/AUTOGEN/OTPSEND".format(api_key=api_key, phone=phone)
#             response = requests.request("GET", url)
#             data = response.json()
#             request.session['user_session_data'] = data['Details']
#             hash_token = UserSession.objects.create(user=user)
#             request.session["user_session_uuid"] = str(hash_token.uuid)
#             return redirect("accounts:otp_input")
#
#     else:
#         return render(request, 'accounts/register.html', {'form': form})
#
#
# class HomeView(LoginRequiredMixin, TemplateView):
#     template_name = 'accounts/home.html'
