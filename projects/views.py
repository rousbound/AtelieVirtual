from django.shortcuts import render
from projects.models import Project
import os
import sys
module_dir = os.path.dirname(__file__)  

def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'project_index.html', context)

def project_detail(request, title):
    project = Project.objects.get(title=title)
    htmlpath = project.title + ".html"
    context = {
        'project': project,
        'htmlpath' : htmlpath
    }
    return render(request, 'project_detail.html', context)


def get_busList(path):
    data_file = open(path, 'r')       
    busList = []
    for line in data_file:
      busList.append(line.strip().split(","))
    return busList



def project_detail_bus(request):
    file_path = os.path.join(module_dir, 'static/LiveTracking/BusesPos.txt')

    busList = get_busList(file_path)

    project = Project.objects.get(title = 'CataÔnibus')
    context = {
        'project': project,
        'buses': busList
    }
    return render(request, 'project_detail_bus.html', context)
