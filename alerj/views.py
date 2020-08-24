from django.shortcuts import render
from alerj.models import PL
import os

module_dir = os.path.dirname(__file__)  

def alerj_index(request):

    pls = PL.objects.all()
    context = {
        "pls": pls,
            }
    return render(request, "alerj_index.html", context)

def pl_detail(request, id):

    pl = PL.objects.get(pk=id)
    project = pl.project.replace("/","_")
    filepath = f"lei_{project}.html"
    return render(request, filepath)
