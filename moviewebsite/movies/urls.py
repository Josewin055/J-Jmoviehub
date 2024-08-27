# # moviewebsite/urls.py
#
# from django.contrib import admin
# from django.urls import path
# from movies import views as movie_views
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', movie_views.home, name='home'),
#     path('register/', movie_views.register, name='register'),
#     path('add_movie/', movie_views.add_movie, name='add_movie'),
#     path('movie/<int:movie_id>/', movie_views.movie_detail, name='movie_detail'),
# ]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='movies/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('profile/',views.user_profile, name='user_profile'),
    path('movie/<int:movie_id>/edit/',views.edit_movie,name='edit_movie'),
    path('movie/<int:id>/delete/',views.delete_movie,name='delete_movie'),
    path('logout/', views.logout, name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:id>/', views.movie_detail, name='movie_detail'),
    path('category/<slug:slug>/', views.category_movies, name='category_movies'),
    path('search/', views.search_movies, name='search'),
]


