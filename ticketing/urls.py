from django.urls import path

from . import views

urlpatterns = [
    path('movie/list/', views.movie_list),
    path('cinema/list/', views.cinema_list),
]
