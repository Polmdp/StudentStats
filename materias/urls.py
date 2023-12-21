from os import path

from materias import views

app_name="materias"
urlpatterns=[
    path("lista_materias/", views.ListaMaterias.as_view(), name="lista-materias"),
    path("detail/<int:id>/",views.detallemateria,name="detail-materia"),
    path("editamateria-<int:id>/",views.editarmateria,name="edita-materia")
]
