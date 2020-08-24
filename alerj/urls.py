from django.urls import path
from . import views

urlpatterns = [
    path("", views.alerj_index, name="alerj_index"),
    path("<int:id>", views.pl_detail, name="pl_detail")
]

