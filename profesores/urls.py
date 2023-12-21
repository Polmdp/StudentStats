from os import path

from . import views

app_name="profesores"
urlpatterns=[
    path("lista_profesores/",views.ListaProfesores.as_view(),name="lista-profesores"),
    path("agrega_profesor/",views.agrega_profesor,name="agrega-profesor"),
    path("detail_profesor/<int:id>/", views.detalleprofesor, name="detail-profesor"),
    path("editaprofesor-<int:id>/", views.editarprofesor, name="edita-profesor-form"),
    ]