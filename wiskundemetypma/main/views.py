from .models import myUserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from oefenen.models import OpdrachtVoortgang, Vaardigheid, Onderwerp, Opgave, Voortgang, Gebruiker, Uitleg
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

            linkbase = "/oefenen/"
            try:
                if Uitleg.objects.get(vaardigheid=v):
                    linkbase = "/oefenen/uitleg/"
            except ObjectDoesNotExist:
                pass

            lijst.append(v.naam)
            try:
                voortgang = Voortgang.objects.get(vaardigheid=v, user=user)
                soortvaardigheid[o.letter]['vaardigheid'].append({"naam": v.naam, "voortgang" : voortgang.voortgang, "link" : linkbase + o.letter + "/" + str(v.nummer)})

            except ObjectDoesNotExist:
                soortvaardigheid[o.letter]['vaardigheid'].append({"naam": v.naam, "voortgang" : 0.0, "link" : linkbase + o.letter + "/" + str(v.nummer)})   
    
    soortvaardigheid = json.dumps(soortvaardigheid)
    
    return render(request, "main/gebruiker.html", {
        "user": username,
        "soortvaardigheid": soortvaardigheid,
        "message" : message,
        "status": status,
    })

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Herstel je wachtwoord"
					email_template_name = "main/passwords/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'help.wvy@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('/blog')
					return HttpResponseRedirect("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/passwords/password_reset.html", context={"password_reset_form":password_reset_form})