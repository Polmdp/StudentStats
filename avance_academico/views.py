from urllib import request

import form
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import ProfesorModel, MateriaModel

# Create your views here.

from django.views import generic
from .models import Materia, Profesor, Estudiante


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
        estudiante=Estudiante.objects.get(user=self.request.user)
        return estudiante.materias_aprobadas.order_by("-anio")
class ListaProfesores(generic.ListView):
    template_name="avance_academico/profesor_list.html"
    context_object_name = "profesor_list"
    def get_queryset(self):
        return Profesor.objects.order_by("nombre_profesor")[:10]



def detalleprofesor(request,id):
    profesor=get_object_or_404(Profesor,pk=id)
    return render(request,"avance_academico/detail_profesor.html",{"profesor":profesor})


def get_name(request):
    if request.method == "POST":
        form_model=ProfesorModel(request.POST)
        if form_model.is_valid():
            profesor=form_model.save()
            return redirect("avance_academico:detail-profesor",profesor.id)


    else:
        form = ProfesorModel()

    return render(request, "avance_academico/agrega-profesor.html", {"form": form})
def editProfesor(request, id):
    profesor = Profesor.objects.get(pk=id)
    if request.method=="POST":
        form_model=ProfesorModel(request.POST,instance=profesor)
        if form_model.is_valid():
            form_model.save()
            return redirect("avance_academico:detail-profesor", profesor.id)
    else:
        form = ProfesorModel(instance=profesor)

    return render(request, "avance_academico/agrega-profesor.html", {"form": form})

def editMateria(request,id):
    materia = Materia.objects.get(pk=id)
    if request.method=="POST":
        form_model=MateriaModel(request.POST,instance=materia)
        if form_model.is_valid():
            form_model.save()
            return redirect("avance_academico:detail-materia", materia.id)
    else:
        form=MateriaModel(instance=materia)
    return render(request,template_name="avance_academico/EditMateria.html", context={"form":form})
class login(LoginView):
    template_name = "avance_academico/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('avance_academico:index')
    def form_invalid(self, form):
        messages.error(self.request, "login incorrecto")
        return self.render_to_response((self.get_context_data(context={"form": form})))

def detallemateria(request, id):
    materia = get_object_or_404(Materia, pk=id)
    profesor = Profesor.objects.filter(materias=materia.id)
    return render(request, "avance_academico/detail_materia.html", {"materia": materia, "profesores": profesor})
class Inscripcion(generic.ListView):
    template_name = "avance_academico/inscripcion.html"
    context_object_name = "materia_list"

    def get_queryset(self):
        estudiante=Estudiante.objects.get(user=self.request.user)
        materias=Materia.objects.exclude(id__in=estudiante.materias_aprobadas.all())
        return materias.order_by("anio")
    def get_querysetinscripcion(self):
        estudiante = Estudiante.objects.get(user=request.user)
        materias_aprobadas=estudiante.materias_aprobadas.all()


def confirmacioninscripcion(request,id):
    estudiante = Estudiante.objects.get(user=request.user)
    materia = get_object_or_404(Materia, pk=id)
    correlativas = materia.correlativas.all()
    materias_aprobadas = estudiante.materias_aprobadas.all().order_by("anio")
    cont=0
    for correlativa in correlativas:
        if correlativa in materias_aprobadas:
            cont+=1
    if cont== len(correlativas):
        estudiante.materias_en_curso.add(materia)
        return render(request,template_name="avance_academico/ConfirmacionInscripcion.html")
    else:
        return render(request,template_name="avance_academico/error.html")

