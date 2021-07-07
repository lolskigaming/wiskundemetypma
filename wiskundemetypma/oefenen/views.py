from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import OpdrachtVoortgang, Vaardigheid, Onderwerp, Opgave, Voortgang, Gebruiker, Uitleg, Tijdsfactor
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import datetime

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
    o = Onderwerp.objects.get(letter=letter.capitalize())
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
        'u':u
    })

# Bepaal de volgende opdracht
def volgende(request):
    # Als er nagekeken is...
    if request.method == "POST":
        # sla wat data op
        score = float(request.POST["score"])
        o = Onderwerp.objects.get(letter=request.POST["letter"].capitalize())
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
        nieuwe_voortgang = float(vo.voortgang) + (score / float(g.intensiteit))
        if nieuwe_voortgang > 1.5:
            nieuwe_voortgang = 1.5
        elif nieuwe_voortgang < -0.5:
            nieuwe_voortgang = -0.5

        # Sla dat op
        vo.voortgang = nieuwe_voortgang
        vo.save()

        # Als de gebruiker de vaardigheid beheerst
        if nieuwe_voortgang >= 1:
            # Stuur hem door naar het keuzemenu voor de volgende vaardigheid
            aantalvaardigheden = len(Voortgang.objects.filter(user=user, voortgang__gte=0.9))
            totaal = len(Vaardigheid.objects.all())-1 # (null vaardigheid telt niet mee)
            score = aantalvaardigheden / totaal * 100
            print(f'score = {aantalvaardigheden} / {totaal} = {score}')
            
            g.score = score
            g.save()

            return render(request, "oefenen/volgende.html", {
                "v":v.volgende.all()
            })
        # Als de gebruiker teveel fout heeft
        if nieuwe_voortgang <= -0.5:
            # Doe voor nu niks, maar later wordt dit een redirect naar de uitleg
            return HttpResponseRedirect(reverse('uitleg', kwargs={
                'letter':v.bijbehorend_onderwerp.letter,
                'pk':v.nummer
            }))
        # Moet hij dezelfde vaardigheid blijven oefenen, herlaad de pagina
        return HttpResponseRedirect(reverse('oefenen', kwargs={
                'letter':v.bijbehorend_onderwerp.letter,
                'pk':v.nummer
                }))        
    
    # Komt de gebruiker met een GET-method, dan is er iets fout gegaan
    return render(request, "oefenen/volgende.html", {
            "score":"huh"
        })

# Render de uitleg pagina voor de juiste vaardigheid
@login_required
def uitleg(request, letter, pk):
    # Sla wat data op
    uid = request.user.id
    user = User.objects.get(id=uid)
    o = Onderwerp.objects.get(letter=letter.capitalize())
    v = Vaardigheid.objects.get(bijbehorend_onderwerp=o, nummer=pk)

    # Haal de juiste uitleg uit de database
    uitleg = Uitleg.objects.get(vaardigheid=v)

    # Stuur de data door naar de template
    return render(request, "oefenen/uitleg.html", {
        'uitleg':uitleg,
        'letter':letter,
        'pk':pk
    })

# Render het overzicht van een onderwerp + alle voortgang per vaardigheid
@login_required
def overzicht(request, letter):
    # Sla wat data op
    o = Onderwerp.objects.get(letter=letter.capitalize())
    v = Vaardigheid.objects.filter(bijbehorend_onderwerp=o)
    user = User.objects.get(id=request.user.id)

    # Maak een lijst met daarin voor elke vaardigheid een tuple met als waardes (vaardigheid, voortgang)
    vaardigheid = list()
    for each in v:
        try:
            voortg = Voortgang.objects.get(vaardigheid=each, user=user)
            # (je kan ook een negatieve voortgang hebben of groter dan 1, maar dat printen we niet)
            if voortg.voortgang < 0:
                vaardigheid.append((each, 0))
                continue
            if voortg.voortgang > 1:
                vaardigheid.append((each, 1))
                continue
            vaardigheid.append((each, voortg.voortgang))
        except:
            vaardigheid.append((each, 0))

    # Stuur alle data door naar de goede template
    return render(request, "oefenen/overzicht.html", {
        "v":vaardigheid
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
    
    # Bereken waarmee we de delta moeten vermenigvuldigen
    procent_per_dag = float(100 / factor.intensiteit)
    intensiteit = procent_per_dag / 100

    # Haal alle voortgang uit de database op
    alles = Voortgang.objects.all()

    # Haal er voor elke voortgang 1 procent af (per dag)
    for elke in alles:
        # Als het percentage 0 of lager is, doe niks
        if elke.voortgang > 0:
            nieuw = elke.voortgang - (delta * intensiteit)
            if nieuw >= 0:
                elke.voortgang = nieuw
                elke.save()
                continue
            # Als de nieuwe voortgang kleiner is dan 0, maak er gewoon 0 van
            elke.voortgang = 0
            elke.save()

    # Sla op dat we vandaag deze functie runden
    factor.laatste_keer = vandaag
    factor.save()
