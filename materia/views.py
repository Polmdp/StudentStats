from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from materia.forms import MateriaModel
from materia.models import Materia


# Create your views here.
class ListaMaterias(generic.ListView):
    template_name="avance_academico/materias_list.html"
    context_object_name = "materia_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Materia.objects.order_by("anio")[:50]
def detallemateria(request,id):
    materia = get_object_or_404(Materia, pk=id)
    return render(request, "avance_academico/template/materia/detail_materia.html", {"materia": materia})
def editMateria(request,id):
    if request.method=="POST":
        materia=Materia.objects.get(pk=id)
        form_model=MateriaModel(request.POST,instance=materia)
        if form_model.is_valid():
            form_model.save()
            return redirect("avance_academico:detail-materia", materia.id)
    else:
        form=MateriaModel()
    return render(request, template_name="avance_academico/template/materia/EditMateria.html", context={"form":form})