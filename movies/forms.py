from django import forms
from .models import MovieCard

class MovieCardForm(forms.ModelForm):
    class Meta:
        model = MovieCard
        fields = ['title', 'description', 'image', 'external_link']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'ckeditor'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Размер изображения не должен превышать 5 МБ")
        return image
