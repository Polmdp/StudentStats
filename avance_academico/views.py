import json
from tkinter import INSERT
from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from pyexpat.errors import messages

from .forms import  ProfesorModel, MateriaModel

# Create your views here.

from django.views import generic
from .models import Materia, Profesor,Estudiante,MateriaCursada,Calificacion
import networkx as nx


def Estadocarrera(request):
        estudiante = Estudiante.objects.get(user=request.user)
        cant_materias= len(Materia.objects.all())
        materias_aprobadas=len(MateriaCursada.objects.filter(aprobada=True,estudiante=estudiante).all())
        porcentaje=materias_aprobadas/cant_materias*100
        return render(request,"avance_academico/estado-carrera.html",{"estudiante":estudiante,"cant_materias":cant_materias,"cant_aprobadas":materias_aprobadas,"porcentaje":porcentaje})


def VerificaIncripcion(request, id):
    estudiante = Estudiante.objects.get(user=request.user)
    materia = get_object_or_404(Materia, pk=id)
    correlativas = materia.correlativas.all()
    correlativas_no_aprobadas = correlativas.exclude( id__in=MateriaCursada.objects.filter(estudiante=estudiante, aprobada=True).values_list('materia_id', flat=True))
    if not correlativas_no_aprobadas:
        MateriaCursada.objects.create(estudiante=estudiante, materia=materia)
        return redirect("avance_academico:index")
    else:
        return render(request, template_name="avance_academico/error-anotacion.html",
                      context={"correlativas_no_aprobadas": correlativas_no_aprobadas})

class AnotaMaterias(LoginRequiredMixin,generic.ListView):
    template_name = "avance_academico/anotarse-materias.html"
    context_object_name = "materias_disponibles"
    def get_queryset(self):
        estudiante= Estudiante.objects.get(user=self.request.user)
        materias_no_disponibles=MateriaCursada.objects.filter(estudiante=estudiante)
        materias_no_disponibles_ids = [materia_cursada.materia_id for materia_cursada in materias_no_disponibles]
        materias = Materia.objects.exclude(id__in=materias_no_disponibles_ids)
        return materias
class MyLoginView(LoginView):
    template_name = "avance_academico/login.html"
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('avance_academico:index')
    def form_invalid(self, form):

        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class IndexView(generic.ListView):
    template_name = "avance_academico/index.html"
    context_object_name = ""

    def get_queryset(self):
        """Return the last five published questions."""
        return Materia.objects.order_by("-anio")[:50]


class ListaMaterias(LoginRequiredMixin,generic.ListView):
    template_name = "avance_academico/materias_list.html"
    context_object_name = "materia_list"

    def get_queryset(self):
        """Muestra materias"""
        estudiante= Estudiante.objects.get(user=self.request.user)
        materias_aprobadas=MateriaCursada.objects.filter(estudiante_id=estudiante.id,aprobada=1)
        materias_aprobadas_ids = [materia_cursada.materia_id for materia_cursada in materias_aprobadas]
        materias=Materia.objects.filter(id__in=materias_aprobadas_ids)
        return materias

class ListaProfesores(LoginRequiredMixin,generic.ListView):
    template_name = "avance_academico/profesor_list.html"
    context_object_name = "profesor_list"

    def get_queryset(self):
        return Profesor.objects.order_by("nombre_profesor")[:10]


def detallemateria(request, id):
    materia = get_object_or_404(Materia, pk=id)
    profesores=Profesor.objects.filter(materias=materia.id)
    materia_cursada=MateriaCursada.objects.get(materia=materia)
    calificaciones=Calificacion.objects.filter(materia_cursada_id=materia_cursada.id)
    grafo = construir_grafo(id)
    grafo_json = grafo_to_json(grafo)
    return render(request, "avance_academico/detail_materia.html", {"materia": materia,"profesores":profesores,"calificaciones":calificaciones,"grafo_json":grafo_json})


def detalleprofesor(request, id):
    profesor = get_object_or_404(Profesor, pk=id)
    return render(request, "avance_academico/detail_profesor.html", {"profesor": profesor})


def agrega_profesor(request):
    if request.method == "POST":
        # form = ProfesorForm(request.POST)
        form_model = ProfesorModel(request.POST)
        if form_model.is_valid():
            # nombre=form.cleaned_data['nombre']
            # apellido=form.cleaned_data['apellido']
            # profesor=Profesor.objects.create(nombre_profesor=nombre,apellido_profesor=apellido)

            profesor = form_model.save()

            return redirect("avance_academico:detail-profesor", profesor.id)

    else:
        form = ProfesorModel()

    return render(request, "avance_academico/edita-datos.html", {"form": form})


class FiltraProfesor(generic.ListView):
    template_name = "avance_academico/edita-profesor.html"
    context_object_name = "profesor_list"

    def get_queryset(self):
        return Profesor.objects.order_by("nombre_profesor")[:10]


def editarprofesor(request, id):
    profesor = Profesor.objects.get(pk=id)

    if request.method == "POST":
        form_model = ProfesorModel(request.POST, instance=profesor)
        if form_model.is_valid():
            form_model.save()
            return redirect("avance_academico:detail-profesor", profesor.id)
    else:
        form = ProfesorModel(instance=profesor)

    return render(request, "avance_academico/edita-datos.html", {"form": form})
def editarmateria(request,id):
    materia = Materia.objects.get(pk=id)

    if request.method == "POST":
        form_model = MateriaModel(request.POST, instance=materia)
        if form_model.is_valid():
            form_model.save()
            return redirect("avance_academico:detail-materia", materia.id)
    else:
        form = MateriaModel(instance=materia)

    return render(request, "avance_academico/edita-datos.html", {"form": form})
def construir_grafo(materia_id):
    grafo = nx.DiGraph()
    materias = Materia.objects.filter(id=materia_id)

    def agregar_correlativas(materia):
        for correlativa in materia.correlativas.all():
            grafo.add_edge(correlativa.nombre, materia.nombre)
            agregar_correlativas(correlativa)

    for materia in materias:
        grafo.add_node(materia.nombre)
        agregar_correlativas(materia)

    return grafo



def grafo_to_json(grafo):
    nodes = [{"id": node, "label": node} for node in grafo.nodes()]
    edges = [{"from": u, "to": v} for u, v in grafo.edges()]
    return json.dumps({"nodes": nodes, "edges": edges})


