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


from .models import User, Room, Guests

# Create your views here.

@csrf_exempt
def index(request):
    
    return render(request, "hotel/index.html", {'n' : range(1, 35), 'total': 34 })


def info(request):
    
    return render(request, "hotel/info.html")


@csrf_exempt
def availability(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    checkInDate = data.get("checkindate","")
    checkOutDate = data.get("checkoutdate","")

    if len(checkInDate) == 0:
        return JsonResponse({"error": "empty post."}, status=400)

    if len(checkOutDate) == 0:
        return JsonResponse({"error": "empty post."}, status=400)

    return JsonResponse({'single': 2, 'double': 8}, status=201)


@csrf_exempt
def bookings(request):

    single = Room.objects.get(roomtype='S')
    double = Room.objects.get(roomtype='D')
    triple = Room.objects.get(roomtype='T')
    quadruple = Room.objects.get(roomtype='Q')
    
    return render(request, "hotel/bookings.html", {'single': single.rate, 
                                                   'double': double.rate,
                                                   'triple': triple.rate,
                                                   'quadruple': quadruple.rate})



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
