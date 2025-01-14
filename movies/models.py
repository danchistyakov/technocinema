from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class MovieCard(models.Model):
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='movies/', null=True, blank=True)
    external_link = models.URLField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def total_votes(self):
        return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_card = models.ForeignKey(MovieCard, related_name='votes', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_card')