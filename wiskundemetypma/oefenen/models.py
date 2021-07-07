from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from ckeditor.fields import RichTextField
from django.contrib import admin

# Create your models here.

# Dit slaat onderwerpen op, zoals "differentiëren" of "meetkunde", met een
class Onderwerp(models.Model):
    # naam en letter
    naam = models.CharField(max_length=128)
    letter = models.CharField(max_length=4, default="A")
    # link naar de eerste vaardigheid
    start = models.ForeignKey("oefenen.Vaardigheid", on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.naam

# Dit slaat de losse vaardigheden op, zoals "lineaire vergelijkingen oplossen", met een
class Vaardigheid(models.Model):
    # naam en nummer
    naam = models.CharField(max_length=255, blank=False, null=True)
    nummer = models.IntegerField(blank=True, null=True)
    # bij behorend onderwerp
    bijbehorend_onderwerp = models.ForeignKey(Onderwerp, on_delete=models.PROTECT, blank=True, null=True)
    # lijst met voorkennis van vaardigheden
    voorkennis = models.ManyToManyField("self", symmetrical=False, related_name="vaardigheid_voorkennis")
    # lijst met volgende vaardigheden
    volgende = models.ManyToManyField("self", symmetrical=False, related_name="vaardigheid_volgende")

    def __str__(self):
        return self.bijbehorend_onderwerp.letter + ". " + self.naam + "  (" + str(self.nummer) + ")"

    class Meta:
        ordering = ['bijbehorend_onderwerp', 'nummer']

# Dit slaat een opdracht op, zoals "Los op. 3x = 6", met een
class Opgave(models.Model):
    # opgave
    opgave = RichTextField()
    # evt. een plaatje
    plaatje = models.ImageField(blank=True, null=True, upload_to='images/')
    # link naar de vaardigheid waar hij bij hoort
    vaardigheid = models.ForeignKey(Vaardigheid, on_delete=models.PROTECT)
    # uitwerking
    uitwerking = RichTextField()

    def __str__(self):
        return "Opgave bij " + self.vaardigheid.naam + " - " + str(self.pk)
    
    class Meta:
        ordering = ['vaardigheid', 'pk']

# Dit slaat bij een gebruiker de overall score en intensiteit op 
class Gebruiker(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    score = models.FloatField(default=0)
    intensiteit = models.IntegerField(default=3)

# Dit slaat per vaardigheid per gebruiker de voortgang op (tussen -1 en 1,5)
class Voortgang(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    vaardigheid = models.ForeignKey(Vaardigheid, on_delete=models.PROTECT)
    voortgang = models.FloatField(default=0)
    
    def __str__(self):
        return "Voortgang van " + str(self.user) + " voor " + str(self.vaardigheid) + " is " + str(self.voortgang)

class OpdrachtVoortgang(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    opdracht = models.ForeignKey(Opgave, on_delete=PROTECT)
    hoevaak_gedaan = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + " heeft de opdracht \"" + self.opdracht.opgave + "\" " + str(self.hoevaak_gedaan) + " keer gedaan"

class Uitleg(models.Model):
    vaardigheid = models.OneToOneField(Vaardigheid, on_delete=models.PROTECT)
    uitleg = RichTextField()
    voorbeeld = RichTextField(null=True, blank=True)

    def __str__(self):
        return "Uitleg voor " + self.vaardigheid.naam

class Tijdsfactor(models.Model):
    laatste_keer = models.DateField()
    intensiteit = models.IntegerField(default=100)


