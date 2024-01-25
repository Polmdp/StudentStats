import json
from datetime import datetime, time, timedelta, date
from urllib import request

import networkx as nx
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_GET
from pyexpat.errors import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import ProfesorModel, MateriaModel
from .models import Materia, Profesor, Estudiante, MateriaCursada, Calificacion, ConfiguracionSemestre


from rest_framework import serializers
from .models import Materia, Profesor

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ('nombre_profesor', 'apellido_profesor')

class MateriaSerializer(serializers.ModelSerializer):
    profesores = ProfesorSerializer(many=True, read_only=True)
    duracionHoras = serializers.SerializerMethodField()

    class Meta:
        model = Materia
        fields = ('codigo', 'nombre', 'dia', 'inicio_horario', 'fin_horario', 'profesores', 'duracionHoras')

    def get_duracionHoras(self, obj):
        if obj.inicio_horario and obj.fin_horario:
            inicio = datetime.combine(datetime.today(), obj.inicio_horario)
            fin = datetime.combine(datetime.today(), obj.fin_horario)
            duracion = fin - inicio
            return duracion.total_seconds() / 3600
        return 0

@api_view(['GET'])
def get_materias(request):
    estudiante = Estudiante.objects.get(user=request.user)
    materias_encurso = MateriaCursada.objects.filter(estudiante=estudiante, en_curso=1)
    materias_encurso_ids = [materia.materia_id for materia in materias_encurso]
    materias = Materia.objects.filter(id__in=materias_encurso_ids).order_by("inicio_horario").all()
    serializer = MateriaSerializer(materias, many=True)
    return Response(serializer.data)

def cronogramaMaterias(request):
    template_name = "avance_academico/cronograma-materias.html"

    return render(request, template_name)



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
    materias_encurso = MateriaCursada.objects.filter(estudiante=estudiante, en_curso=1)
    materias_encurso_ids = [materia.materia_id for materia in materias_encurso]
    materias = Materia.objects.filter(id__in=materias_encurso_ids).all()
    materias_iguales = materias.filter(dia__contains=materia.dia)
    materias_superpuestas = []
    for materia_tabla in materias_iguales:
        print(materias_iguales)
        if (
                materia.inicio_horario < materia_tabla.fin_horario and materia.inicio_horario >= materia_tabla.inicio_horario) or \
                (
                        materia_tabla.inicio_horario < materia.fin_horario and materia_tabla.inicio_horario >= materia.inicio_horario):
            materias_superpuestas.append(materia_tabla)

    if len(materias_superpuestas) > 0:
        mensaje = f"Error en la inscripción, coincide con la(s) materia(s): {', '.join(str(materia.nombre) for materia in materias_iguales)}"
        return JsonResponse({
            "success": False,
            "message": mensaje,
        })
    else:
        MateriaCursada.objects.create(estudiante=estudiante, materia=materia, en_curso=1)
        return JsonResponse({"success": True})


class AnotaMaterias(LoginRequiredMixin, generic.ListView):
    template_name = "avance_academico/anotarse-materias.html"
    context_object_name = "materias_disponibles"

    def get_queryset(self):
        estudiante = Estudiante.objects.get(user=self.request.user)
        materias_no_disponibles = MateriaCursada.objects.filter(estudiante=estudiante)
        materias_no_disponibles_ids = [materia_cursada.materia_id for materia_cursada in materias_no_disponibles]
        fechas_semestre = ConfiguracionSemestre.obtener_fechas_actuales()
        fecha_actual = datetime.now().date()

        if fecha_actual <= fechas_semestre["fin_primer_cuatri"]:
            materias = Materia.objects.exclude(id__in=materias_no_disponibles_ids).exclude(
                duracion="SEGUNDO CUATRIMESTRE")

        elif fecha_actual < fechas_semestre["inicio_segundo_cuatri"] or fecha_actual > fechas_semestre[
            "fin_segundo_cuatri"]:
            materias = []
        else:
            materias = Materia.objects.exclude(id__in=materias_no_disponibles_ids).filter(
                duracion="SEGUNDO CUATRIMESTRE")
        materias_disponibles = []
        for materia in materias:
            correlativas = materia.correlativas.all()
            correlativas_no_aprobadas = correlativas.exclude(
                id__in=MateriaCursada.objects.filter(estudiante=estudiante, aprobada=True).values_list('materia_id',
                                                                                                       flat=True))
            if not correlativas_no_aprobadas:
                materias_disponibles.append(materia)
        return materias_disponibles


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
