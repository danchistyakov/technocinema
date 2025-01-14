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
            return redirect('home')  # Перенаправляем на главную страницу
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


@login_required
def vote_movie_card(request, card_id):
    if request.method == "POST":
        movie_card = get_object_or_404(MovieCard, id=card_id)

        # Нельзя голосовать за свою карточку
        if movie_card.author == request.user:
            return JsonResponse({'status': 'error', 'message': 'Нельзя голосовать за свою карточку'}, status=403)

        # Получение значения голоса
        data = json.loads(request.body)
        vote_value = data.get('vote')
        if vote_value not in [1, -1]:
            return JsonResponse({'status': 'error', 'message': 'Неверное значение голоса'}, status=400)

        # Проверка, голосовал ли уже пользователь
        vote, created = Vote.objects.get_or_create(user=request.user, movie_card=movie_card)
        if not created and vote.value == vote_value:
            return JsonResponse({'status': 'error', 'message': 'Вы уже голосовали таким образом'}, status=400)

        # Обновление или создание голоса
        vote.value = vote_value
        vote.save()

        return JsonResponse({'success': True, 'new_vote_count': movie_card.total_votes()})
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'}, status=400)
