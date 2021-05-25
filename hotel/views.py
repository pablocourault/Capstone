import json 
from django.utils import translation
from django.utils.translation import activate
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from django.db.models import Sum
from .models import User, Room, Guests, Bookings

# Create your views here.

@csrf_exempt
def index(request):

    # variables n and total are used to pic gallery
    return render(request, "hotel/index.html", {'n' : range(1, 35), 'total': 34 })


def info(request):
    
    return render(request, "hotel/info.html")


@csrf_exempt
def bookings(request):

    single_rate = Room.objects.get(roomtype='S').rate
    double_rate = Room.objects.get(roomtype='D').rate
    triple_rate = Room.objects.get(roomtype='T').rate
    quadruple_rate = Room.objects.get(roomtype='Q').rate


    if request.method != "POST":
        initial_range = range(0, 1)

        return render(request, "hotel/bookings.html", { 'label': '',
                                                        'single_range': initial_range,
                                                        'double_range': initial_range,
                                                        'triple_range': initial_range,
                                                        'quadruple_range': initial_range,
                                                        'single_rate': single_rate, 
                                                        'double_rate': double_rate,
                                                        'triple_rate': triple_rate,
                                                        'quadruple_rate': quadruple_rate })

    else:

        # required interval of availability 
        checkInDate = request.POST["datein"]
        checkOutDate = request.POST["dateout"]

        # get the total quantity of room by type (single, double, triple and quadruple)
        single_quantity = Room.objects.get(roomtype='S').quantity
        double_quantity = Room.objects.get(roomtype='D').quantity
        triple_quantity = Room.objects.get(roomtype='T').quantity
        quadruple_quantity = Room.objects.get(roomtype='Q').quantity

        # count quantity of room reserved in the request interval
        # each query evaluates a possible overlap, and counts the reservations 
        single_reserved_query1 = Bookings.objects.filter(checkin_date__gte=checkInDate, checkout_date__gte=checkOutDate, checkin_date__lte=checkOutDate).aggregate(Sum('singles'))
        single_reserved_query2 = Bookings.objects.filter(checkin_date__lte=checkInDate, checkout_date__gte=checkOutDate).aggregate(Sum('singles'))
        single_reserved_query3 = Bookings.objects.filter(checkin_date__lte=checkInDate, checkout_date__lte=checkOutDate, checkout_date__gte=checkInDate).aggregate(Sum('singles'))
        single_reserved1 = single_reserved_query1['singles__sum']        
        single_reserved2 = single_reserved_query2['singles__sum']
        single_reserved3 = single_reserved_query3['singles__sum']

        single_reserved = 0
        
        if (single_reserved1 != None):
            single_reserved = single_reserved1
        
        if (single_reserved2 != None):
            single_reserved = single_reserved + single_reserved2
        
        if (single_reserved3 != None):
            single_reserved = single_reserved + single_reserved3

        # compute total of singles rooms availables
        if (single_reserved != None):
            single_available = single_quantity - single_reserved
        else:
            single_available = single_quantity
        
        # count quantity of type double room reserved in the request interval
        # each query evaluates a possible overlap, and counts the reservations
        double_reserved_query1 = Bookings.objects.filter(checkin_date__gte=checkInDate).filter(checkout_date__gte=checkOutDate, checkin_date__lte=checkOutDate).aggregate(Sum('doubles'))
        double_reserved_query2 = Bookings.objects.filter(checkin_date__lte=checkInDate).filter(checkout_date__gte=checkOutDate).aggregate(Sum('doubles'))
        double_reserved_query3 = Bookings.objects.filter(checkin_date__lte=checkInDate).filter(checkout_date__lte=checkOutDate, checkout_date__gte=checkInDate).aggregate(Sum('doubles'))
        double_reserved1 = double_reserved_query1['doubles__sum']
        double_reserved2 = double_reserved_query2['doubles__sum']
        double_reserved3 = double_reserved_query3['doubles__sum']


        double_reserved = 0

        if (double_reserved1 != None):
            double_reserved = double_reserved1
        
        if (double_reserved2 != None):
            double_reserved = double_reserved + double_reserved2
        
        if (double_reserved3 != None):
            double_reserved = double_reserved + double_reserved3

        # compute total of doubles rooms availables
        if (double_reserved != None):
            double_available = double_quantity - double_reserved
        else:
            double_available = double_quantity


        # count quantity of type triple room reserved in the request interval
        # each query evaluates a possible overlap, and counts the reservations
        triple_reserved_query1 = Bookings.objects.filter(checkin_date__gte=checkInDate).filter(checkout_date__gte=checkOutDate, checkin_date__lte=checkOutDate).aggregate(Sum('triples'))
        triple_reserved_query2 = Bookings.objects.filter(checkin_date__lte=checkInDate).filter(checkout_date__gte=checkOutDate).aggregate(Sum('triples'))
        triple_reserved_query3 = Bookings.objects.filter(checkin_date__lte=checkInDate).filter(checkout_date__lte=checkOutDate, checkout_date__gte=checkInDate).aggregate(Sum('triples'))
        triple_reserved1 = triple_reserved_query1['triples__sum']
        triple_reserved2 = triple_reserved_query2['triples__sum']
        triple_reserved3 = triple_reserved_query3['triples__sum']

        triple_reserved = 0

        if (triple_reserved1 != None):
            triple_reserved = triple_reserved1
        
        if (triple_reserved2 != None):
            triple_reserved = triple_reserved + triple_reserved2
        
        if (triple_reserved3 != None):
            triple_reserved = triple_reserved + triple_reserved3

        # compute total of triples typpe rooms availables
        if (triple_reserved != None):
            triple_available = triple_quantity - triple_reserved
        else:
            triple_available = triple_quantity

        quadruple_reserved_query1 = Bookings.objects.filter(checkin_date__gte=checkInDate).filter(checkout_date__gte=checkOutDate, checkin_date__lte=checkOutDate).aggregate(Sum('quadruples'))
        quadruple_reserved_query2 = Bookings.objects.filter(checkin_date__lte=checkInDate).filter(checkout_date__gte=checkOutDate).aggregate(Sum('quadruples'))
        quadruple_reserved_query3 = Bookings.objects.filter(checkin_date__lte=checkInDate).filter(checkout_date__lte=checkOutDate, checkout_date__gte=checkInDate).aggregate(Sum('quadruples'))
        quadruple_reserved1 = quadruple_reserved_query1['quadruples__sum']
        quadruple_reserved2 = quadruple_reserved_query2['quadruples__sum']
        quadruple_reserved3 = quadruple_reserved_query3['quadruples__sum']

        quadruple_reserved = 0

        if (quadruple_reserved1 != None):
            quadruple_reserved = quadruple_reserved1
        
        if (quadruple_reserved2 != None):
            quadruple_reserved = quadruple_reserved + quadruple_reserved2
        
        if (quadruple_reserved3 != None):
            quadruple_reserved = quadruple_reserved + quadruple_reserved3

        # compute total of quadruple type rooms availables
        if (quadruple_reserved != None):
            quadruple_available = quadruple_quantity - quadruple_reserved
        else:
            quadruple_available = quadruple_quantity

        # ranges of rooms availables by type to pass to the selects in booking.html
        single_range = range(0, single_available + 1)
        double_range = range(0, double_available + 1)
        triple_range = range(0, triple_available + 1)
        quadruple_range = range(0, quadruple_available + 1)

        return render(request, "hotel/bookings.html", { 'label': 'availables',
                                                        'check_in_date': checkInDate,
                                                        'check_out_date': checkOutDate,
                                                        'single_range': single_range,
                                                        'double_range': double_range,
                                                        'triple_range': triple_range,
                                                        'quadruple_range': quadruple_range,
                                                        'single_rate': single_rate, 
                                                        'double_rate': double_rate,
                                                        'triple_rate': triple_rate,
                                                        'quadruple_rate': quadruple_rate,
                                                        'single_available': single_available,
                                                        'double_available': double_available,
                                                        'triple_available': triple_available,
                                                        'quadruple_available': quadruple_available })



def facilities(request):
    
    return render(request, "hotel/facilities.html")


def houserules(request):
    
    return render(request, "hotel/houserules.html")


def finalprint(request):
    
    return render(request, "hotel/finalprint.html")


def guestsreviews(request):
    
    return render(request, "hotel/guestsreviews.html")


def faqs(request):
    
    return render(request, "hotel/faqs.html")


@csrf_exempt
def language(request):

    user_language = request.POST["language"]
    translation.activate(user_language)  
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

    return render(request, "hotel/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "hotel/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "hotel/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "hotel/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "hotel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hotel/register.html")
