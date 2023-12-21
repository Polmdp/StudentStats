from django.urls import path

from . import views

app_name = "avance_academico"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("lista_materias/", views.ListaMaterias.as_view(), name="lista-materias"),
    path("lista_profesores/",views.ListaProfesores.as_view(),name="lista-profesores"),
    path("agrega_profesor/",views.get_name,name="agrega-profesor"),
    path("detail/<int:id>/",views.detallemateria,name="detail-materia"),
    path("detail_profesor/<int:id>/",views.detalleprofesor,name="detail-profesor"),
    path("modificaprof/<int:id>/",views.editProfesor,name="editaprofesor"),
    path("modifica/<int:id>/",views.editMateria,name="editamateria"),
    path("inscribirse/",views.Inscripcion.as_view(),name="inscripcion"),
    path("confirmacion/<int:id>/",views.confirmacioninscripcion,name="confirmacion"),
    path("confirmacion/",views.confirmacioninscripcion,name="error")
]
