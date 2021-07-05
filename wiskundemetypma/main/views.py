from .models import myUserCreationForm
from django.shortcuts import render
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
                HttpResponseRedirect(next)
            return HttpResponseRedirect("/blog") # BLOG IS TIJDELIJKKKKK!!!!!!!!!!
        else:
            return render(request, "main/inloggen.html") # ERROR MESSAGE MOET ER NOG BIJJJJ!!!!!
    else:
        return render(request, "main/inloggen.html")

def registreren(request):
    if request.method == "POST":
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/blog.html') # Error and succession yet to come
    else:
        form = myUserCreationForm()
    return render(request, 'main/registreren.html', {'form':form})

def over(request):
    return render(request, "main/over.html")

def leaderboard(request):
    return render(request, "main/leaderboard.html")