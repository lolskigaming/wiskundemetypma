from .models import myUserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from oefenen.models import OpdrachtVoortgang, Vaardigheid, Onderwerp, Opgave, Voortgang, Gebruiker
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
import json

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
                return HttpResponseRedirect(next)
            request.session["message"] = "Je bent ingelogd!"
            request.session["status"] = 1
            return HttpResponseRedirect(reverse('gebruiker'))
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
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                gebruiker = Gebruiker(user=User.objects.get(id=request.user.id))
                gebruiker.save()
                print(gebruiker)
                return render(request, 'main/gebruiker.html',{
                    "message": "je bent nu geregistreerd!",
                    "status": 1
                })

            
            return render(request, 'main/gebruiker.html',{
                "message": "Je bent nu geregistreerd! Maar er is wel iets misgegaan met het inloggen, probeer opnieuw in te loggen.",
                "status": 0
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


@login_required
def leaderboard(request):
    return render(request, "main/leaderboard.html")

@login_required
def gebruiker(request):
    user = User.objects.get(id=request.user.id)
    username = request.user.username
    onderwerp = Onderwerp.objects.all()
    soortvaardigheid = dict()

    try:
        message = request.session["message"]
        request.session["message"] = None
        status = request.session["status"]
        request.session["status"] = None
    except:
        message = "An error has occured which we did not handle"
        status = None
    
    for o in onderwerp:
        
        if o.letter == 'Z':
            continue
        vaardigheid = Vaardigheid.objects.filter(bijbehorend_onderwerp=o)
        lijst = list()
        
        soortvaardigheid[o.letter] = {'vaardigheid' : [], 'naam' : o.naam}
        
        for v in vaardigheid:
            lijst.append(v.naam)
            try:
                voortgang = Voortgang.objects.get(vaardigheid=v, user=user)
                print(voortgang.voortgang)
                soortvaardigheid[o.letter]['vaardigheid'].append({"naam": v.naam, "voortgang" : voortgang.voortgang, "link" : "/oefenen/uitleg/" + o.letter + "/" + str(v.nummer)})
            except ObjectDoesNotExist:
                soortvaardigheid[o.letter]['vaardigheid'].append({"naam": v.naam, "voortgang" : 0.0, "link" : "/oefenen/uitleg/" + o.letter + "/" + str(v.nummer)})
        
    
    soortvaardigheid = json.dumps(soortvaardigheid)
    
    return render(request, "main/gebruiker.html", {
        "user": username,
        "soortvaardigheid": soortvaardigheid,
        "message" : message,
        "status": status,
    })