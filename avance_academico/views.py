from urllib import request

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.

from django.views import generic


class IndexView(generic.ListView):
    template_name = "avance_academico/index.html"
    context_object_name = ""



