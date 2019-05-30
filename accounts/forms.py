from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from . models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import password_validation
from django.conf import settings


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=14, widget=forms.TextInput(attrs={"class": "input-medium bfh-phone", "data-format": "+91dddddddddd"}))


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=14, widget=forms.TextInput(attrs={"class": "input-medium bfh-phone", "data-format": "+91dddddddddd"}))

    class Meta:
        model = User
        fields = ('phone', 'email', 'password1', 'password2',)


class PasswordResetForm(forms.Form):

    phone = forms.CharField(max_length=14, widget=forms.TextInput(attrs={"class": "input-medium bfh-phone", "data-format": "+91dddddddddd"}))

    class Meta:
        fields = ('phone', )


class PasswordResetNewForm(forms.Form):

    otp = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1==password2:
            return self.cleaned_data
        else:
            raise ValidationError("Both password must be same.")

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)


    class Meta:
        fields = ('otp', 'password1', 'password2')


class OTPForm(forms.Form):
    otp = forms.IntegerField()

    class Meta:
        fields = ('otp', )
