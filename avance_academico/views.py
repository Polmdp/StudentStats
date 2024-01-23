import json
from datetime import datetime
from tkinter import INSERT
from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from pyexpat.errors import messages

from django import forms
from .forms import ProfesorModel, MateriaModel

# Create your views here.

from django.views import generic
from .models import Materia, Profesor, Estudiante, MateriaCursada, Calificacion
import networkx as nx


def ValidaDatos(request):
    return render(request, "avance_academico/valida-datos.html")


def errorAnotacion(materias_faltantes):
    return render(request, template_name="avance_academico/error-anotacion.html",
                  context={"correlativas_no_aprobadas": materias_faltantes})


def Estadocarrera(request):
    estudiante = Estudiante.objects.get(user=request.user)
    cant_materias = len(Materia.objects.all())
    materias_aprobad = MateriaCursada.objects.filter(aprobada=True, estudiante=estudiante).all()
    materias_aprobadas = len(materias_aprobad)
    porcentaje = materias_aprobadas / cant_materias * 100
    aprobadas_finales = Calificacion.objects.filter(tipo="FINAL", nota__gte=4)
    if request.method == "POST":
        form = Cantaños(request.POST)
        cursa_materias = form.data.get("cant_años")
        cant_años_calculados = int((cant_materias - materias_aprobadas) / int(cursa_materias))

        return render(request, "avance_academico/estado-carrera.html",
                      {"estudiante": estudiante, "cant_materias": cant_materias,
                       "materias_aprobadas": materias_aprobad, "cant_aprobadas": materias_aprobadas,
                       "porcentaje": porcentaje, "aprobadas_finales": aprobadas_finales, "form": form,
                       "cant_años_calculados": cant_años_calculados})
    else:
        form = Cantaños()
        return render(request, "avance_academico/estado-carrera.html",
                      {"estudiante": estudiante, "cant_materias": cant_materias,
                       "materias_aprobadas": materias_aprobad, "cant_aprobadas": materias_aprobadas,
                       "porcentaje": porcentaje, "aprobadas_finales": aprobadas_finales, "form": form,
                       })


def VerificaIncripcion(request, id):
    estudiante = Estudiante.objects.get(user=request.user)
    materia = get_object_or_404(Materia, pk=id)
    correlativas = materia.correlativas.all()
    correlativas_no_aprobadas = correlativas.exclude(
        id__in=MateriaCursada.objects.filter(estudiante=estudiante, aprobada=True).values_list('materia_id', flat=True))

    materias_encurso=MateriaCursada.objects.filter(estudiante=estudiante, en_curso=1)
    materias_encurso_ids = [materia.materia_id for materia in materias_encurso]
    materias = Materia.objects.filter(id__in=materias_encurso_ids).all()
    materias_iguales = materias.filter(horario__contains=materia.horario, dia__contains=materia.dia)

    if materias_iguales.exists():
        mensaje = f"Error en la inscripción, coincide con la(s) materia(s): {', '.join(str(materia.nombre) for materia in materias_iguales)}"
        return JsonResponse({
            "success": False,
            "message": mensaje,
        })
    else:
        if not correlativas_no_aprobadas:
            MateriaCursada.objects.create(estudiante=estudiante, materia=materia, en_curso=1)

            return JsonResponse({"success": True})

        else:
            lista_materias_nombre = [correlativa.nombre for correlativa in correlativas_no_aprobadas]
            return JsonResponse({
                "success": False,
                "message": "Error en la inscripción",
                "details": {"correlativas_no_aprobadas": lista_materias_nombre}
            })


class AnotaMaterias(LoginRequiredMixin, generic.ListView):
    template_name = "avance_academico/anotarse-materias.html"
    context_object_name = "materias_disponibles"

    def get_queryset(self):
        estudiante = Estudiante.objects.get(user=self.request.user)
        materias_no_disponibles = MateriaCursada.objects.filter(estudiante=estudiante)
        materias_no_disponibles_ids = [materia_cursada.materia_id for materia_cursada in materias_no_disponibles]
        fecha_actual = datetime.now()
        fecha_limite_primercuatri = datetime(2024, 4, 1)
        fecha_inicio_segundocuatri = datetime(2024, 7, 1)
        fecha_limite_segundocuatri = datetime(2024, 7, 25)
        if fecha_actual <= fecha_limite_primercuatri:
            materias = Materia.objects.exclude(id__in=materias_no_disponibles_ids).exclude(
                duracion="SEGUNDO CUATRIMESTRE")

        elif fecha_actual < fecha_inicio_segundocuatri or fecha_actual > fecha_limite_segundocuatri:
            materias = []
        else:
            materias = Materia.objects.exclude(id__in=materias_no_disponibles_ids).filter(
                duracion="SEGUNDO CUATRIMESTRE")

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


@require_GET
def buscar_materia(request):
    query = request.GET.get('q', '')
    if query:
        materias = Materia.objects.filter(nombre__icontains=query)
    else:
        materias = Materia.objects.none()

    resultados = [{'id': materia.id, 'nombre': materia.nombre} for materia in materias]
    return JsonResponse(resultados, safe=False)


class ListaMaterias(LoginRequiredMixin, generic.ListView):
    template_name = "avance_academico/materias_list.html"
    context_object_name = "materia_list"

    def get_queryset(self):
        """Muestra materias"""
        estudiante = Estudiante.objects.get(user=self.request.user)
        materias_aprobadas = MateriaCursada.objects.filter(estudiante_id=estudiante.id, aprobada=1)
        materias_aprobadas_ids = [materia_cursada.materia_id for materia_cursada in materias_aprobadas]
        materias = Materia.objects.filter(id__in=materias_aprobadas_ids)
        return materias


class MuestraMaterias(generic.ListView):
    template_name = "avance_academico/materias_carrera.html"
    context_object_name = "materia_list"

    def get_queryset(self):
        return Materia.objects.order_by("nombre")[:50]


class ListaProfesores(LoginRequiredMixin, generic.ListView):
    template_name = "avance_academico/profesor_list.html"
    context_object_name = "profesor_list"

    def get_queryset(self):
        return Profesor.objects.order_by("nombre_profesor")[:10]


def detallemateria(request, id):
    materia = get_object_or_404(Materia, pk=id)
    profesores = Profesor.objects.filter(materias=materia.id)

    grafo = construir_grafo(id)
    grafo_json = grafo_to_json(grafo)
    return render(request, "avance_academico/detail_materia.html",
                  {"materia": materia, "profesores": profesores,
                   "grafo_json": grafo_json})


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
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect("avance_academico:detail-profesor", profesor.id)
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(form_model.errors, status=400)
    else:
        form = ProfesorModel(instance=profesor)

    return render(request, "avance_academico/edita-datos.html", {"form": form})


def editarmateria(request, id):
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


class Cantaños(forms.Form):
    cant_años = forms.IntegerField(label="Cantidad de materias que desea cursar", max_value=20, min_value=1)
