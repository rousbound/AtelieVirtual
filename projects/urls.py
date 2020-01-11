from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),
    path("7/", views.project_detail_bus, name="project_detail_bus"),
    path("9/", views.project_detail_snake, name="project_detail_snake"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
]
