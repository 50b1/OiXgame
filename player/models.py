from django.db import models

from django.contrib.auth.models import User


class Zaproszenie(models.Model):
    od_usera = models.ForeignKey(User, related_name='zaproszenie_wyslane', on_delete=models.CASCADE)
    do_usera = models.ForeignKey(
        User, 
        related_name='zaproszenie_odebrane', 
        verbose_name='Użytkownik do zaproszenia', 
        help_text='Wybierz Użytkownika z którym chcesz rozegrać grę.',
        on_delete=models.CASCADE
        )
    wiadomosc = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Opcjonalna wiadomość', 
        help_text='Zawsze dobrze powiedzieć coś miłego ;)'
        )
    czas_wiadomosci = models.DateTimeField(auto_now_add=True)
