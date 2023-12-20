from django.forms import ModelForm

from avance_academico.models import Materia


class MateriaModel(ModelForm):
    class Meta:
        model= Materia
        fields="__all__"