from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import MovieCardForm
from django.http import JsonResponse

from .models import MovieCard, Vote
import json


@login_required
def create_movie_card(request):
    if request.method == 'POST':
        form = MovieCardForm(request.POST, request.FILES)
        if form.is_valid():
            movie_card = form.save(commit=False)
            movie_card.author = request.user
            movie_card.save()
            return redirect('home')
    else:
        form = MovieCardForm()
    return render(request, 'movies/create_movie_card.html', {'form': form})


@login_required
def delete_movie_card(request, card_id):
    if request.method == "POST":
        card = get_object_or_404(MovieCard, id=card_id, author=request.user)
        card.is_deleted = True
        card.save()
        return JsonResponse({'success': True, 'message': 'Карточка удалена'})
    return JsonResponse({'success': False, 'message': 'Неверный запрос'}, status=400)


def vote_movie_card(request, card_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': "Авторизуйтесь чтобы проголосовать за карточку фильма."},
                                status=401)

        movie_card = get_object_or_404(MovieCard, id=card_id)

        if movie_card.author == request.user:
            return JsonResponse({'success': False, 'message': 'Нельзя голосовать за свою карточку'}, status=403)

        data = json.loads(request.body)
        vote_value = data.get('vote')
        if vote_value not in [1, -1]:
            return JsonResponse({'success': False, 'message': 'Неверное значение голоса'}, status=400)

        vote, created = Vote.objects.get_or_create(user=request.user, movie_card=movie_card)
        if not created and vote.value == vote_value:
            return JsonResponse({'success': False, 'message': 'Вы уже голосовали таким образом'}, status=400)

        vote.value = vote_value
        vote.save()

        return JsonResponse({'success': True, 'new_vote_count': movie_card.total_votes()})
    return JsonResponse({'success': False, 'message': 'Неверный запрос'}, status=400)
