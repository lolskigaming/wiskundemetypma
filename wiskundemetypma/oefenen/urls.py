from django.urls import path
from .  import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:letter>/<int:pk>", views.oefenen, name="oefenen")
]
