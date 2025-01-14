# Generated by Django 4.2.17 on 2025-01-14 15:57

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_moviecard_vote_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='movie',
            new_name='movie_card',
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'movie_card')},
        ),
        migrations.RemoveField(
            model_name='moviecard',
            name='vote_count',
        ),
        migrations.AddField(
            model_name='vote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vote',
            name='value',
            field=models.IntegerField(),
        ),
    ]
