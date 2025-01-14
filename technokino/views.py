from django.shortcuts import render
from movies.models import MovieCard

from django.contrib.sessions.models import Session

def home(request):
    cards = MovieCard.objects.filter(is_deleted=False).order_by('-created_at')
    return render(request, 'home.html', {'cards': cards})
