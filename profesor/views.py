from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from profesor.forms import ProfesorModel
from profesor.models import Profesor


# Create your views here.
class ListaProfesores(generic.ListView):
    template_name= "avance_academico/../profesor/template/profesor/profesor_list.html"
    context_object_name = "profesor_list"
    def get_queryset(self):
        return Profesor.objects.order_by("nombre_profesor")[:10]

def detalleprofesor(request,id):
    profesor=get_object_or_404(Profesor,pk=id)
    return render(request, "avance_academico/../profesor/template/profesor/detail_profesor.html", {"profesor":profesor})


def get_name(request):
    if request.method == "POST":
        form_model=ProfesorModel(request.POST)

        if form_model.is_valid():
            profesor=form_model.save()
            return redirect("avance_academico:detail-profesor",profesor.id)


    else:
        form = ProfesorModel()

    return render(request, "avance_academico/../profesor/template/profesor/agrega-profesor.html", {"form": form})
def editProfesor(request,id):
    if request.method=="POST":
        profesor=Profesor.objects.get(pk=id)
        form_model=ProfesorModel(request.POST,instance=profesor)
        if form_model.is_valid():
            form_model.save()
            return redirect("avance_academico:detail-profesor", profesor.id)
    else:
        form = ProfesorModel()

    return render(request, "avance_academico/../profesor/template/profesor/agrega-profesor.html", {"form": form})

