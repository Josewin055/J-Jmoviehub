# movies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify  # Import slugify function


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    trailer_link = models.URLField()
    poster = models.ImageField(upload_to='posters/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Make sure this field is defined

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Ensure slugify is used
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()  # For simplicity, assuming rating is an integer
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.movie.title}'