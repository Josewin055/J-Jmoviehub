# movies/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .models import Movie, Review, Category
from .forms import MovieForm, ReviewForm
from datetime import datetime
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator,EmptyPage,InvalidPage


def home(request):
    current_year = datetime.now().year
    categories = Category.objects.all()
    # Assuming you have a Movie model
    movies = Movie.objects.all()
    paginator=Paginator(movies,8)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'categories':Category.objects.all(),
        'movies': movies,
        'current_year': current_year,
        'categories': categories
    }
    return render(request, 'movies/home.html', context)

def category_movies(request, slug):
    category = get_object_or_404(Category, slug=slug)
    movies = Movie.objects.filter(category=category)
    return render(request, 'movies/category_movies.html', {'category': category, 'movies': movies})
@login_required(login_url='movies:login')
def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:movie_detail', id=id)
    else:
        form = ReviewForm()

    reviews = movie.reviews.all()  # Get all reviews for the movie
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'form': form, 'reviews': reviews})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('movies:home')  # Redirect to the home page or any other page
    else:
        form = UserCreationForm()
    return render(request, 'movies/register.html', {'form': form})

@login_required
def user_profile(request):
    user_movies=Movie.objects.filter(added_by=request.user)
    return render(request,'movies/profile.html',{'user_movies': user_movies})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, added_by=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_detail', id=movie.id)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/edit_movie.html', {'form': form, 'movie': movie})

@login_required
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id, added_by=request.user)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:home')
    return render(request, 'movies/confirm_delete.html', {'movie': movie})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'movies/login.html', {'form': form})

@login_required(login_url='movies:login')
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(user=request.user)  # Pass the current user
            return redirect('movies:home')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})

# def movie_detail(request, movie_id):
#     movie = Movie.objects.get(id=movie_id)
#     reviews = movie.reviews.all()
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST)
#         if review_form.is_valid():
#             review = review_form.save(commit=False)
#             review.user = request.user
#             review.movie = movie
#             review.save()
#             return redirect('movie_detail', movie_id=movie_id)
#     else:
#         review_form = ReviewForm()
#     return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews, 'review_form': review_form}


def search_movies(request):
    query = request.GET.get('q')
    results = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, 'movies/search_results.html', {'results': results, 'query': query})

def logout(request):
    auth_logout(request)
    return redirect('movies:home')
