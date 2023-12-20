from django import forms
from django.forms import ModelForm

from .models import Profesor, Materia


class ProfesorForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido = forms.CharField(label="Apellido", max_length=100)
    dni = forms.CharField(label="Dni", max_length=8)


class ProfesorModel(ModelForm):
    class Meta:
        model = Profesor
        fields = "__all__"
class MateriaModel(ModelForm):
    class Meta:
        model=Materia
        fields="__all__"
