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
    path("editamateria-<int:id>/",views.editarmateria,name="edita-materia"),
    path("anotamateria",views.AnotaMaterias.as_view(),name="anota-materias"),
    path("comprobacion<int:id>/",views.VerificaIncripcion,name="verifica-inscripcion"),
    path("estado_carrera/",views.Estadocarrera,name="estado-carrera"),
    path("validadatos/",views.ValidaDatos,name="ingresa-datos"),
    path('buscar_materia', views.buscar_materia, name='buscar_materia'),
    path("materias_carrera",views.MuestraMaterias.as_view(),name="muestra_materias"),
    path("error/",views.errorAnotacion,name="error_anotacion")

]
