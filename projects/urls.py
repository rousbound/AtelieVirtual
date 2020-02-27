from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),
    path("CariocaScript/", views.project_detail_carioca, name="project_detail_carioca"),
    path("EscolaVirtual/", views.project_detail_escola, name="project_detail_escola"),
    path("CataÔnibus/", views.project_detail_bus, name="project_detail_bus"),
    path("CifraVirtual/", views.project_detail_cifra, name="project_detail_cifra"),
    path("Darwin/", views.project_detail_snake, name="project_detail_snake"),
    path("<str:title>/", views.project_detail, name="project_detail"),
    #path("<int:pk>/", views.project_detail, name="project_detail"),
]
