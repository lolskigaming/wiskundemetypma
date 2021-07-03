from django.urls import path
from .  import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blog", views.blog, name="blog"),
    path("inloggen", views.inloggen, name="inloggen"),
    path("registreren", views.registreren, name="registreren"),
    path("over", views.over, name="over"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
]
