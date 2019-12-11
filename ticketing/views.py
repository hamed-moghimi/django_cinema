from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Movie, Cinema, ShowTime, Ticket


def movie_list(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'ticketing/movie_list.html', context)


def cinema_list(request):
    cinemas = Cinema.objects.all()
    context = {
        'cinemas': cinemas
    }
    return render(request, 'ticketing/cinema_list.html', context)


def movie_details(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {
        'movie': movie
    }
    return render(request, 'ticketing/movie_details.html', context)


def cinema_details(request, cinema_id):
    cinema = Cinema.objects.get(pk=cinema_id)
    context = {
        'cinema': cinema
    }
    return render(request, 'ticketing/cinema_details.html', context)


def showtime_list(request):
    showtimes = ShowTime.objects.all().order_by('start_time')
    context = {
        'showtimes': showtimes
    }
    return render(request, 'ticketing/showtime_list.html', context)


@login_required
def showtime_details(request, showtime_id):
    showtime = ShowTime.objects.get(pk=showtime_id)
    context = {
        'showtime': showtime
    }
    if request.method == 'POST':
        try:
            seat_count = int(request.POST['seat_count'])
            assert showtime.status == showtime.SALE_OPEN, 'فروش بلیت برای این سانس ممکن نیست.'
            assert showtime.free_seats >= seat_count, 'این سانس به اندازه کافی صندلی خالی ندارد.'
            price = showtime.price * seat_count
            assert request.user.profile.spend(price), 'اعتبار شما برای خرید بلیت کافی نیست.'
            showtime.reserve_seats(seat_count)
            ticket = Ticket.objects.create(showtime=showtime, customer=request.user.profile, seat_count=seat_count)
        except Exception as e:
            context['error'] = str(e)
        else:
            return HttpResponseRedirect(reverse('ticketing:ticket_details', kwargs={'ticket_id': ticket.id}))
    return render(request, 'ticketing/showtime_details.html', context)


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user.profile).order_by('-order_time')
    context = {
        'tickets': tickets
    }
    return render(request, 'ticketing/ticket_list.html', context)


@login_required
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    context = {
        'ticket': ticket
    }
    return render(request, 'ticketing/ticket_details.html', context)
