from django.forms import ModelForm

from .models import Profesor


class ProfesorModel(ModelForm):
    class Meta:
        model = Profesor
        fields = "__all__"
