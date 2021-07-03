from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Vaardigheid, Onderwerp

# Create your views here.
# Maak een lijst van alle onderwerpen en een linkje naar hun start
def index(request):
    o = Onderwerp.objects.all()
    onderwerpen = list()
    for each in o:
        naam = each.naam
        if naam == "NULL":
            continue
        letter = each.letter
        v = each.start
        pk = int(v.nummer)
        onderwerpen.append([naam, letter, pk])

    return render(request, "oefenen/index.html", {
        'onderwerpen':onderwerpen
    })