from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

from gameplay.models import Game
from .forms import ZaproszenieFormularz
from .models import Zaproszenie


@login_required
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    finished_games = my_games.difference(active_games)
    invitations = request.user.zaproszenie_odebrane.all()

    return render(request, "player/home.html",
                    {'games': active_games,
                    'finished_games': finished_games,
                    'invitations': invitations})



@login_required
def nowe_zaproszenie(request):
    if request.method == 'POST':
        invitation = Zaproszenie(od_usera=request.user)
        form = ZaproszenieFormularz(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = ZaproszenieFormularz()
    return render(request, 'player/nowe_zaproszenie_form.html', {'form': form})


@login_required
def akceptuj_zaproszenie(request, id):
    invitation = get_object_or_404(Zaproszenie, pk=id)
    if not request.user == invitation.do_usera:
        raise PermissionDenied
    if request.method == 'POST':
        if 'accept' in request.POST:
            game = Game.objects.create(
                first_player = invitation.do_usera,
                second_player = invitation.od_usera,
            )
        invitation.delete()
        return redirect(game)
    else:
        return render(request, 'player/akceptuj_zaproszenie_form.html', {'invitation': invitation})


class ZarejestrujSie(CreateView):
    form_class = UserCreationForm
    template_name = "player/rejestracja.html"
    success_url = reverse_lazy('player_home')
