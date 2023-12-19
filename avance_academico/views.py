from urllib import request

from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.views import generic
from .models import Materia,Profesor


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
class ListaProfesores(generic.ListView):
    template_name="avance_academico/profesor_list.html"
    context_object_name = "profesor_list"
    def get_queryset(self):
        return Profesor.objects.order_by("nombre_profesor")[:10]
def detallemateria(request,id):
    materia = get_object_or_404(Materia, pk=id)
    return render(request, "avance_academico/detail_materia.html", {"materia": materia})
def detalleprofesor(request,id):
    profesor=get_object_or_404(Profesor,pk=id)
    return render(request,"avance_academico/detail_profesor.html",{"profesor":profesor})

