from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),
    path("Programs/", views.project_index, name="program_index"),
    path("CataÔnibus/", views.project_detail_bus, name="project_detail_bus"),
    path("<str:title>/", views.project_detail, name="project_detail"),
]
