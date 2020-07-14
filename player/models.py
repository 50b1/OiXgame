from django.db import models

from django.contrib.auth.models import User


class Zaproszenie(models.Model):
    od_usera = models.ForeignKey(User, related_name='zaproszenie_wyslane')
    do_usera = models.ForeignKey(User, related_name='zaproszenie_odebrane')
    wiadomosc = models.CharField(max_length=300)
    czas_wiadomosci = models.DateTimeField(auto_now_add=True)
