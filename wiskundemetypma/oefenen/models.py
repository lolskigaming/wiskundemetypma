from django.db import models

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