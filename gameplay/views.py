from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from .models import Game
from .forms import MoveForm

@login_required
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    context = {'game': game}
    if game.kogo_ruch(request.user):
        context['form'] = MoveForm()
    return render(request, "gameplay/game_detail.html", context)
    

@login_required
def zrob_move(request, id):
    game = get_object_or_404(Game, pk=id)
    if not game.kogo_ruch(request.user):
        raise PermissionDenied
    move = game.nowy_move()
    form = MoveForm(instance=move, data=request.POST)
    if form.is_valid():
        move.save()
        return redirect('gameplay_detale', id)
    else:
        return render(request, 'gameplay/game_detail.html', {'game': game, 'form': form})

class ListaWszystkichGier(ListView):
    model = Game
