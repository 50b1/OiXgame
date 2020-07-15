from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse


GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw'),
)

ROZMIAR_PLANSZ =3

class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):

        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )

class Game(models.Model):

    first_player = models.ForeignKey(User, related_name="games_first_player")
    second_player = models.ForeignKey(User, related_name="games_second_player")

    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices = GAME_STATUS_CHOICES)

    objects = GamesQuerySet.as_manager()
    

    def __str__(self):
        return "{0} vs {1} Game".format(self.first_player, self.second_player)

    def get_absolute_url(self):
        return reverse('gameplay_detale', args=[self.id])

    def plansza(self):
        """Zwraca 2 wymiarowa liste Ruchow, mozna zapytac o stan pola w pozycji [y][x]"""
        
        plansza = [[None for x in range(ROZMIAR_PLANSZ)] for y in range(ROZMIAR_PLANSZ)]
        for move in self.move_set.all():
            plansza[move.y][move.x] = move
        return plansza



class Move(models.Model):

    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField(editable=False)

    game=models.ForeignKey(Game, on_delete=models.CASCADE, editable=False)