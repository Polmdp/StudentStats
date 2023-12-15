from urllib import request

from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.views import generic
from .models import Materia


class IndexView(generic.ListView):
    template_name = "avance_academico/index.html"
    context_object_name = ""
    def get_queryset(self):
        """Return the last five published questions."""
        return Materia.objects.order_by("-anio")[:50]



class ListaMaterias(generic.ListView):
    template_name="avance_academico/materias_list.html"
    context_object_name = "materia_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Materia.objects.order_by("anio")[:50]

def detallemateria(request,id):
    materia = get_object_or_404(Materia, pk=id)
    return render(request, "avance_academico/detail_materia.html", {"materia": materia})




