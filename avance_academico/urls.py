from django.urls import path

from . import views

app_name = "avance_academico"
urlpatterns = [
path("", views.IndexView.as_view(), name="index"),
 path("\n", views.ListaMaterias.as_view(), name="lista-materias"),
 path("specifics/<int:id>/",views.detallemateria,name="detalle_materia")


]