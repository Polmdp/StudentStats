from django.forms import ModelForm

from materias.models import Materia


class MateriaModel(ModelForm):
    class Meta:
        model = Materia
        fields = "__all__"
