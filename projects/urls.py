from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),
    path("5/", views.project_detail_carioca, name="project_detail_carioca"),
    path("6/", views.project_detail_escola, name="project_detail_escola"),
    path("7/", views.project_detail_bus, name="project_detail_bus"),
    path("8/", views.project_detail_cifra, name="project_detail_cifra"),
    path("9/", views.project_detail_snake, name="project_detail_snake"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
]
