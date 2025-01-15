from django.shortcuts import render
from movies.models import MovieCard
from django.core.paginator import Paginator

def home(request):
    cards = MovieCard.objects.filter(is_deleted=False).order_by('-created_at')
    paginator = Paginator(cards, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})