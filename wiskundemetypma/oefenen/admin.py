from django.contrib import admin
from .models import Vaardigheid, Onderwerp, Opgave, Voortgang, Gebruiker, OpdrachtVoortgang, Uitleg, Tijdsfactor
import modelclone

# Register your models here.
admin.site.register(Vaardigheid)
admin.site.register(Onderwerp)

class OpgaveAdmin(modelclone.ClonableModelAdmin):
    save_as = True
admin.site.register(Opgave, OpgaveAdmin)
admin.site.register(Voortgang)
admin.site.register(Gebruiker)
admin.site.register(OpdrachtVoortgang)
admin.site.register(Uitleg)
admin.site.register(Tijdsfactor)