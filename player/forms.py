from django.forms import ModelForm
from .models import Zaproszenie


class ZaproszenieFormularz(ModelForm):
    class Meta:
        model = Zaproszenie
        exclude = ('od_usera', 'czas_wiadomosci')
