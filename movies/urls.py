from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('create/', views.create_movie_card, name='create_movie_card'),
    path('delete/<int:card_id>/', views.delete_movie_card, name='delete_movie_card'),
    path('vote/<int:card_id>/', views.vote_movie_card, name='vote_movie_card'),
]

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)