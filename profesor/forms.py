from django.forms import ModelForm

from avance_academico import forms
from avance_academico.models import Profesor


class ProfesorForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    apellido=forms.CharField(label="Apellido",max_length=100)
    dni=forms.CharField(label="Dni",max_length=8)



class ProfesorModel(ModelForm):
    class Meta:
        model = Profesor
        fields = "__all__"
