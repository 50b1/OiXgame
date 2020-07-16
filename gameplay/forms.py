from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Move

class MoveForm(ModelForm):
    class Meta:
        model = Move
        exclude = []

    def czyste(self):
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        game = self.instance.game
        try:
            if game.plansza()[y][x] is not None:
                raise ValidationError("Pole nie jest puste")
        except IndexError:
            raise ValidationError("Nieprawidlowe dane pola!")
        return self.cleaned_data
