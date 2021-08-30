from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import OpdrachtVoortgang, Vaardigheid, Onderwerp, Opgave, Voortgang, Gebruiker, Uitleg, Tijdsfactor
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import datetime
import json

# Create your views here.

# Maak een lijst van alle onderwerpen en een linkje naar hun start
def index(request):
    # Haal alle onderwerpen uit de database
    o = Onderwerp.objects.all()
    # Maak een lijst van al de onderwerpen
    onderwerpen = list()
    for each in o:
        naam = each.naam
        # Is de naam NULL, sla hem over
        if naam == "NULL":
            continue
        letter = each.letter
        v = each.start
        pk = int(v.nummer)
        # Elk item in de lijst onderwerpen bestaat uit een lijst met drie waardes: naam, letter en pk
        onderwerpen.append([naam, letter, pk])

    # Render de template index.html
    return render(request, "oefenen/index.html", {
        'onderwerpen':onderwerpen
    })

# Render de juiste opdracht en sla de scores op.
@login_required
def oefenen(request, letter, pk):
    # Sla wat data op
    uid = request.user.id
    user = User.objects.get(id=uid)
    o = Onderwerp.objects.get(letter=letter.upper())
    v = Vaardigheid.objects.get(bijbehorend_onderwerp=o, nummer=pk)

    # Als deze pagina wordt geladen, checken we ook gelijk de tijdsfactor
    tijdsfactor()

    # Als de user hier al eerder is geweest, doe niks; anders, sla maak een nieuwe voortgang voor hem aan
    try:
        g = Voortgang.objects.get(user=user, vaardigheid=v)
    except ObjectDoesNotExist:
        g = Voortgang(user=user, vaardigheid=v)
        g.save()
     
    # Zoek alle opdrachten voor deze vaardigheid uit de database
    opdr = Opgave.objects.filter(vaardigheid=v)
    # In de lijst opdrachten komen de nog niet gemaakte opdrachten
    opdrachten = list()
    # Voor elke opdracht, zoek uit of hij gemaakt is
    for each in opdr:
        try:
            # Als hoevaak_gedaan niet 0 is (en de opdracht dus al gemaakt is)
            if OpdrachtVoortgang.objects.get(user=user, opdracht=each).hoevaak_gedaan != 0:
                # Doe niks, en voeg dus niet toe aan opdrachten
                pass
            else:
                # Anders, voeg wel toe aan de opdrachtenlijst
                opdrachten.append(each)
        # Als het object niet bestaat, is de opdracht nog nooit gemaakt
        except ObjectDoesNotExist:
            # Voeg toe aan de opdrachtenlijst
            opdrachten.append(each)
    # Als er helemaal geen opdrachten zijn gevonden
    if len(opdrachten) == 0:
        # Reset alle hoevaak_gemaakt waardes
        for each in opdr:
            q = OpdrachtVoortgang.objects.get(user=user, opdracht=each)
            q.hoevaak_gedaan = 0
            q.save()
            # en voeg ze toe aan de lijst
            opdrachten.append(each)
        
    # Genereer een random nummer
    x = randint(0, len(opdrachten)-1) 

    # Sla de opdracht op in JSON vorm
    opdracht = {"opdracht":opdrachten[x].opgave,"uitwerking":opdrachten[x].uitwerking}

    try:
        u = Uitleg.objects.get(vaardigheid=v)
    except ObjectDoesNotExist:
        u = None

    # Render de template en stuur de data door
    return render(request, "oefenen/opgave.html", {
        'opdracht':opdrachten[x],
        'o':opdracht,
        'letter':letter,
        'pk':pk,
        'u':u,
        'voortgang': g.voortgang,
        'onderwerp': o.naam,
        'vaardigheid': v.naam,
        'animate': True
    })

def verander_voortgang(voortgang, verandering, max = None):
    nieuwe_voortgang = voortgang.voortgang + verandering

    if nieuwe_voortgang < 0:
        nieuwe_voortgang = 0
    elif nieuwe_voortgang > 100 and voortgang.voortgang < 101:
        nieuwe_voortgang = 100
    elif nieuwe_voortgang > 125 and voortgang.voortgang < 126:
        nieuwe_voortgang = 125
    elif nieuwe_voortgang > 150 and voortgang.voortgang < 151:
        nieuwe_voortgang = 150
    elif nieuwe_voortgang > 175 and voortgang.voortgang < 176:
        nieuwe_voortgang = 175
    elif nieuwe_voortgang > 200:
        nieuwe_voortgang = 200

    if max:
        if nieuwe_voortgang > max:
            nieuwe_voortgang = max

    return nieuwe_voortgang    

# Bepaal de volgende opdracht
def volgende(request):
    # Als er nagekeken is...
    if request.method == "POST":
        # sla wat data op
        score = float(request.POST["score"])
        if score not in range(-2, 3):
            raise ValueError

        o = Onderwerp.objects.get(letter=request.POST["letter"].upper())
        v = Vaardigheid.objects.get(bijbehorend_onderwerp=o, nummer=request.POST["pk"])
        user = User.objects.get(id=request.user.id)
        g = Gebruiker.objects.get(user=user)
        opdracht = Opgave.objects.get(opgave=request.POST["opdracht"])

        # Sla op dat deze opdracht gemaakt is
        try:
            ov = OpdrachtVoortgang.objects.get(user=user, opdracht=opdracht)
            ov.hoevaak_gedaan += 1
            ov.save()

        except:
            ov = OpdrachtVoortgang(user=user, opdracht=opdracht, hoevaak_gedaan=1)
            ov.save()

        # Pas de voortgang van deze vaardigheid aan
        vo = Voortgang.objects.get(user=user, vaardigheid=v)
        huidig = vo.voortgang
        if score == -2:
            vo.voortgang = verander_voortgang(vo, -25)
        elif score == -1:
            if huidig <= 100:
                vo.voortgang = verander_voortgang(vo, -10)
            else:
                vo.voortgang = verander_voortgang(vo, -25)
        elif score == 0:
            pass
        elif score == 1:
            if huidig <= 90:
                vo.voortgang = verander_voortgang(vo, 10, 90)
        elif score == 2:
            if huidig <= 100:
                vo.voortgang = verander_voortgang(vo, 25)
            else:
                vo.voortgang = verander_voortgang(vo, 24)

         # Sla dat op
        vo.save()

        return HttpResponseRedirect(reverse('oefenen', kwargs={
                'letter':v.bijbehorend_onderwerp.letter,
                'pk':v.nummer
                }))        
    
    # Komt de gebruiker met een GET-method, dan is er iets fout gegaan
    return render(request, "oefenen/volgende.html", {
            "score":"huh",
        })

# Render de uitleg pagina voor de juiste vaardigheid
@login_required
def uitleg(request, letter, pk):
    # Sla wat data op
    uid = request.user.id
    user = User.objects.get(id=uid)
    o = Onderwerp.objects.get(letter=letter.upper())
    v = Vaardigheid.objects.get(bijbehorend_onderwerp=o, nummer=pk)

    vaardigheid = list()

    for each in v:
        vaardigheid.append(each.nummer)
    
    # Haal de juiste uitleg uit de database
    uitleg = Uitleg.objects.get(vaardigheid=v[pk-1])

    vaardigheid = json.dumps(vaardigheid)

    # Stuur de data door naar de template
    return render(request, "oefenen/uitleg.html", {
        'uitleg':uitleg,
        'letter':letter,
        'pk':pk,
        'onderwerp': o.naam,
        'vaardigheid': vaardigheid,
        'vaardigheidnaam': v[pk-1].naam,
    })

# Render het overzicht van een onderwerp + alle voortgang per vaardigheid
@login_required
def overzicht(request, letter):
    # Sla wat data op
    o = Onderwerp.objects.get(letter=letter.upper())
    v = Vaardigheid.objects.filter(bijbehorend_onderwerp=o)
    user = User.objects.get(id=request.user.id)

    # Maak een lijst met daarin voor elke vaardigheid een tuple met als waardes (vaardigheid, voortgang)
    vaardigheid = list()
    for each in v:
        try:
            voortg = Voortgang.objects.get(vaardigheid=each, user=user)
            # (je kan ook een negatieve voortgang hebben of groter dan 1, maar dat printen we niet)
            if voortg.voortgang < 0:
                vaardigheid.append([each.naam, each.nummer, 0])
                continue
            if voortg.voortgang >= 0.995:
                vaardigheid.append([each.naam, each.nummer, 1])
                continue
            vaardigheid.append([each.naam, each.nummer, voortg.voortgang])
        except:
            vaardigheid.append([each.naam, each.nummer, 0])
    print(vaardigheid)
    vjson = json.dumps(vaardigheid)
    # Stuur alle data door naar de goede template
    return render(request, "oefenen/overzicht.html", {
        "v":vaardigheid,
        "lijst":vjson,
        "onderwerp": o.naam,
        "letter": o.letter
    })

# Zorg dat er elke dag 1 procent aan voortgang van een vaardigheid afgaat
def tijdsfactor():
    # Sla de laatste keer op dat we de deze functie runden
    factor = Tijdsfactor.objects.all().first()
    # Sla de datum van vandaag op
    vandaag = datetime.date.today()

    # Bereken het verschil in dagen tussen de laatste keer en vandaag
    delta = vandaag - factor.laatste_keer
    delta = delta.days

    # Als dat 0 (of kleiner) is, hoeven we niks te doen
    if delta <= 0:
        return
    
    # Haal alle voortgang uit de database op
    alles = Voortgang.objects.all()

    # Haal er voor elke voortgang 1 procent af (per dag)
    for elke in alles:
        # Als het percentage 0 of lager is, doe niks
        if elke.voortgang in [100, 125, 150, 175]:
            elke.voortgang += 1
            elke.save()

    # Sla op dat we vandaag deze functie runden
    factor.laatste_keer = vandaag
    factor.save()
