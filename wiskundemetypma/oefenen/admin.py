from django.contrib import admin
from .models import Vaardigheid, Onderwerp, Opgave, Voortgang, Gebruiker, OpdrachtVoortgang, Uitleg
# Register your models here.
admin.site.register(Vaardigheid)
admin.site.register(Onderwerp)
admin.site.register(Opgave)
admin.site.register(Voortgang)
admin.site.register(Gebruiker)
admin.site.register(OpdrachtVoortgang)
admin.site.register(Uitleg)