from django import forms
from .models import *
from django.contrib.auth.hashers import *
from Control.models import User,Empresa
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=50,label="Nombre de usuario",widget=forms.TextInput(attrs={'style':'width: 600px ; height:35px;','class':'form-group'}))
    password1 = forms.CharField(max_length=50, label="Contraseña", widget=forms.PasswordInput(attrs={'style': 'width: 600px ; height:35px;', 'class': 'form-group'}))
    password2 = forms.CharField(max_length=50, label="Confirmar", widget=forms.PasswordInput(attrs={'style': 'width: 600px ; height:35px;', 'class': 'form-group'}))
    first_name = forms.CharField(max_length=50,label="Nombre",widget=forms.TextInput(attrs={'style':'width: 600px ; height:35px;','class':'form-group'}))
    last_name = forms.CharField(max_length=50,label="Apellido",widget=forms.TextInput(attrs={'style':'width: 600px ; height:35px;','class':'form-group'}))
    email = forms.EmailField(max_length=150,label="Correo",widget=forms.TextInput(attrs={'style':'width: 600px ; height:35px;','class':'form-group'}))
    emp_id = forms.ModelChoiceField(queryset=Empresa.objects.all(),label="Empresa",widget=forms.Select(attrs={'style':'width: 600px ; height:35px;','class':'form-group'}))
    is_superuser = forms.BooleanField(initial=True,required=False,label="Superusuario",)
    is_active = forms.BooleanField(required=True, initial=True,label="Estado")


