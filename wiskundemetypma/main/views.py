from .models import myUserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def blog(request):
    return render(request, "main/blog.html")

def inloggen(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next = request.POST.get('next')
            if next:
                HttpResponseRedirect(next) # Ik heb dit van vincent gekopieerd, geen idee wat het doet, heb ook geen zin om naar te kijken
            return render(request, "main/blog.html", {
            "message": "we hebben je ingelogd!",
            "status": 1
        }) # BLOG IS TIJDELIJKKKKK!!!!!!!!!!
        else:
            return render(request, "main/inloggen.html",{
                "message": "het wachtwoord en/of de gebruikernsaam klopt niet, probeer het opnieuw",
                "status": -1
            })
    else:
        return render(request, "main/inloggen.html")

def registreren(request):
    if request.method == "POST":
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/blog.html',{
                "message": "je bent nu geregistreerd!",
                "status": 1
            })
        else:
            return render(request, 'main/registreren.html', {
                'form':form,
                "animate": 'False',
                "message": "er is iets mis gegaan met het registreren, probeer het opnieuw.",
                "status": -1
            })
    else:
        form = myUserCreationForm()
    return render(request, 'main/registreren.html', {
        "animate": 'True',
        'form': form
    })

def uitloggen(request):
    logout(request)
    return render(request, 'main/index.html', {
        "message": "je bent uitgelogd!",
        "status": 1
    })

def over(request):
    return render(request, "main/over.html")

def leaderboard(request):
    return render(request, "main/leaderboard.html")