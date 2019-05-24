from django.urls import path

from . import views

app_name = 'ticketing'
urlpatterns = [
    path('movie/list/', views.movie_list, name='movie_list'),
    path('cinema/list/', views.cinema_list, name='cinema_list'),
]
