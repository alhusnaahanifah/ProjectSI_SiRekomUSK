# account/forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'asal_sekolah', 'jenis_kelamin', 'email', 'password1', 'password2']
