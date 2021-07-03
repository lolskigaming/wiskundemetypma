from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def blog(request):
    return render(request, "main/blog.html")

def inloggen(request):
    return render(request, "main/inloggen.html")

def registreren(request):
    return render(request, "main/registreren.html")

def over(request):
    return render(request, "main/over.html")

def leaderboard(request):
    return render(request, "main/leaderboard.html")