from django.urls import path, include
from .  import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blog", views.blog, name="blog"),
    path("inloggen", views.inloggen, name="inloggen"),
    path("registreren", views.registreren, name="registreren"),
    path("over", views.over, name="over"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("home", views.index, name="index"),
    path("uitloggen", views.uitloggen, name="uitloggen"),
    path("gebruiker", views.gebruiker, name="gebruiker"),
    #path("password_reset", views.password_reset_request, name="password_reset")
]
