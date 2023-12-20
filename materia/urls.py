from django.urls import path

from avance_academico import views

urlpatterns = [
    path("lista_materias/", views.ListaMaterias.as_view(), name="lista-materias"),
    path("detail/<int:id>/",views.detallemateria,name="detail-materia"),
    path("modificaMateria/",views.ListaMaterias.as_view(),name="edita-materia"),
    path("modifica/<int:id>/",views.editMateria,name="editamateria")
]