from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:letter>/<int:pk>", views.oefenen, name="oefenen"),
    path("volgende", views.volgende, name="volgende"),
    path("uitleg/<str:letter>/<int:pk>", views.uitleg, name="uitleg"),
    path("overzicht/<str:letter>", views.overzicht, name="overzicht"),
]
