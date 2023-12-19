from urllib import request

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .forms import ProfesorForm

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


def get_name(request):

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ProfesorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfesorForm()

    return render(request, "avance_academico/agrega-profesor.html", {"form": form})
