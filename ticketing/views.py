from django.http import HttpResponse
from django.shortcuts import render

from .models import Movie, Cinema


def movie_list(request):
    movies = Movie.objects.all()
    response_text = '\n'.join(
        '{}: {}'.format(i, movie) for i, movie in enumerate(movies, start=1)
    )
    return HttpResponse(response_text)


def cinema_list(request):
    cinemas = Cinema.objects.all()
    response_text = """
    <html>
    <head>
    <title>لیست سینماها</title>
    </head>
    <body>
        <h1>فهرست سینماهای کشور</h1>
        <ul>
            {}
        </ul>
    </body>
    </html>
    """.format(
        '\n'.join('<li>{}</li>'.format(cinema) for cinema in cinemas)
    )
    return HttpResponse(response_text)
