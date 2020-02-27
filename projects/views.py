from django.shortcuts import render
from projects.models import Project
import os
import sys
module_dir = os.path.dirname(__file__)  
sys.path.insert(0, module_dir + "/static/LiveTracking")
import BusTrack

def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'project_index.html', context)

def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html', context)

def project_detail_escola(request):
    project = Project.objects.get(title = "EscolaVirtual")
    context = {
        'project': project
    }
    return render(request, 'project_detail_escola.html', context)

def project_detail_carioca(request):
    project = Project.objects.get(title="CariocaScript")
    context = {
        'project': project
    }
    return render(request, 'project_detail_carioca.html', context)

def project_detail_cifra(request):
    project = Project.objects.get(title = "CifraVirtual")
    context = {
        'project': project
    }
    return render(request, 'project_detail_cifra.html', context)

def project_detail_snake(request):
    project = Project.objects.get(title = 'Darwin')
    context = {
        'project': project
    }
    return render(request, 'project_detail_snake.html', context)


def get_busList(path):
    data_file = open(path, 'r')       
    busList = []
    for line in data_file:
      busList.append(line.strip().split(","))
    return busList



def project_detail_bus(request):
    BusTrack.get_onibus(module_dir + "/static/LiveTracking/")
    file_path = os.path.join(module_dir, 'static/LiveTracking/BusesPos.txt')

    busList = get_busList(file_path)

    project = Project.objects.get(title = 'CataÔnibus')
    context = {
        'project': project,
        'buses': busList
    }
    return render(request, 'project_detail_bus.html', context)
