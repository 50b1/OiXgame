from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw'),
)

ROZMIAR_PLANSZ = 3

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

    def kogo_ruch(self, user):
        return (user == self.first_player and self.status == 'F') or (user == self.second_player and self.status == 'S')

    def nowy_move(self):
        """Zwraca objekt nowego ruchu z graczem, gra i licza ruchow"""
        if self.status not in 'FS':
            raise ValueError("Nie mozna wykonać ruchu w skonczonej grze")

        return Move(
            game = self,
            by_first_player=self.status == 'F'
        )

    def update_po_move(self, move):
        """Zmienia status po wykonaniu ruchu"""
        self.status = self._get_game_status_after_move(move)

    def _get_game_status_after_move(self, move):
        x, y = move.x, move.y
        plansza = self.plansza()
        if (plansza[y][0] == plansza[y][1] == plansza[y][2]) or (plansza[0][x] == plansza[1][x] == plansza[2][x]) or \
            (plansza[0][0] == plansza[1][1] == plansza[2][2]) or (plansza[0][2] == plansza[1][1] == plansza[2][0]):
            return 'W' if move.by_first_player else 'L'
        if self.move_set.count() >= ROZMIAR_PLANSZ**2:
            return 'D'
        return 'S' if self.status == 'F' else 'F'
            



class Move(models.Model):

    x = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(ROZMIAR_PLANSZ-1)])
    y = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(ROZMIAR_PLANSZ-1)])
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField(editable=False)
    game=models.ForeignKey(Game, on_delete=models.CASCADE, editable=False)

    def __eq__(self, other):
        if other is None:
            return False
        return other.by_first_player == self.by_first_player

    def save(self, *args, **kwargs):
        super(Move, self).save(*args, **kwargs)
        self.game.update_po_move(self)
        self.game.save()
