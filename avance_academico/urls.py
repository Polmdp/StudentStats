from django.urls import path

from . import views

app_name = "avance_academico"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("lista_materias/", views.ListaMaterias.as_view(), name="lista-materias"),
    path("lista_profesores/",views.ListaProfesores.as_view(),name="lista-profesores"),

    path("agrega_profesor/",views.agrega_profesor,name="agrega-profesor"),
    path("detail/<int:id>/",views.detallemateria,name="detail-materia"),
    path("detail_profesor/<int:id>/",views.detalleprofesor,name="detail-profesor"),
    path("editaprofesor-<int:id>/",views.editarprofesor,name="edita-profesor-form"),
    path("editamateria-<int:id>/",views.editarmateria,name="edita-materia")
]
