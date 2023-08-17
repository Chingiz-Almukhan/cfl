import pytz
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from accounts.models import Account
from accounts.utils import send_email_for_verify


class SignUpForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=50,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    psn = forms.CharField(min_length=5, max_length=50,
                          widget=forms.TextInput(attrs={'placeholder': 'Psn', 'class': 'form-control'}))
    email = forms.CharField(min_length=7, max_length=70, required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    avatar = forms.ImageField(required=True)
    password = forms.CharField(label='Password', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', strip=False, required=True,
                                       widget=forms.PasswordInput)
    timezones = [(tz, tz) for tz in pytz.all_timezones]
    timezone = forms.ChoiceField(choices=timezones)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'password_confirm', 'psn', 'avatar', 'timezone')

    def clean(self):
        cleaned_data = super().clean()
        if Account.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError({'email': 'User with this email exist'})
        if Account.objects.filter(email=cleaned_data.get('psn')).exists():
            raise ValidationError({'psn': 'User with this psn exist'})
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Put correct password')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    timezones = [(tz, tz) for tz in pytz.all_timezones]
    timezone = forms.ChoiceField(choices=timezones)

    class Meta:
        model = get_user_model()
        fields = ('psn', 'avatar', 'timezone')


# class LoginForm(forms.Form):
#     username = forms.CharField(required=True, label='Login')
#     password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)

class LoginForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Email not verify, check your email',
                    code='invalid_login',
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
