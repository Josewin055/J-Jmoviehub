# movies/forms.py
# forms.py
from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'actors', 'trailer_link', 'poster', 'category']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True, user=None):
        movie = super().save(commit=False)
        if user:
            movie.added_by = user
        if commit:
            movie.save()
        return movie

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }