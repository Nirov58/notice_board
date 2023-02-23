import secrets
import string

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2", )


class OneTimeCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @staticmethod
    def generate_otc():
        symb_massive = string.ascii_letters + string.digits
        code_array = (secrets.choice(symb_massive) for i in range(6))
        return ''.join(code_array)


class CodeRegisterForm(forms.Form):
    code = forms.CharField(label='Код', max_length=6)
    email = forms.CharField(label='Email', max_length=100)
