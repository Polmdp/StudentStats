from django import forms
from django.forms import ModelForm

from .models import Profesor


class ProfesorForm(forms.Form):
    ombre = forms.CharField(label="Nombre", max_length=100)
    apellido=forms.CharField(label="Apellido",max_length=100)
    dni=forms.CharField(label="Dni",max_length=8)


