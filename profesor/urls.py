from django.urls import path

from avance_academico import views

urlpatterns = [
    path("lista_profesores/",views.ListaProfesores.as_view(),name="lista-profesores"),
    path("agrega_profesor/",views.get_name,name="agrega-profesor"),
    path("detail_profesor/<int:id>/",views.detalleprofesor,name="detail-profesor"),
    path("editar_profesor/",views.ListaProfesores.as_view(),name="edita-profesor"),
    path("modificaprof/<int:id>/",views.editProfesor,name="edita profesor"),
]