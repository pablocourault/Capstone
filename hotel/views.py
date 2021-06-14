import json
from datetime import date
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
from django.db.models import Sum, Avg, Q
from django.core.paginator import Paginator
from .models import User, Room, Guests, Bookings, Consumptions, Services, Comments, Messages


# Create your views here.

@csrf_exempt
def index(request):

    # variables n and total are used to pic gallery
    return render(request, "hotel/index.html", {'n' : range(1, 35), 'total': 34 })


def info(request):
    
    return render(request, "hotel/info.html")

@csrf_exempt
@login_required
def orders(request):

    current_services = Services.objects.all().exclude(description='Rooms')
    is_guest = Guests.objects.filter(guest=request.user).exists()
    
    return render(request, "hotel/orders.html", {'current_services': current_services,
                                                 'is_guest': is_guest})


@csrf_exempt
@login_required
def makeanorder(request):

    data = json.loads(request.body)
    service_id = data.get("service_id","")
    order_quantity = data.get("service_quantity","")

    order_service = Services.objects.get(id=service_id)
    order_guest = Guests.objects.get(guest=request.user)

    order_amount = int(order_quantity) * order_service.rate

    try:
        order_booking = Bookings.objects.get(id=order_guest.booking.id)
        order_booking.amount = order_amount + order_booking.amount
        order_booking.save()

    except IntegrityError:
        return JsonResponse({'message': 'Error in update booking amount.'}, status=401)

    try:

        lenguaje = request.LANGUAGE_CODE
        
        if lenguaje == 'en':
            message_content = order_service.message
        if lenguaje == 'es':
            message_content = order_service.message_es
        if lenguaje == 'pt':
            message_content = order_service.message_pt

        adminhotel = User.objects.get(username='adminhotel')

        new_message = Messages(user= adminhotel,
                               addressee = request.user,
                               message = message_content)
        new_message.save()
        
    except IntegrityError:
        return JsonResponse({'message': 'Error in send order instructions.'}, status=401)

    try:
        order_consumption = Consumptions(user=request.user,
                                         booking= order_guest.booking,
                                         service = order_service,
                                         date = date.today(),
                                         quantity = order_quantity,
                                         amount = order_amount)
        order_consumption.save()
    except IntegrityError:
        return JsonResponse({'message': 'Error in save Order.'}, status=401)
    return JsonResponse({'message': 'Successful Order.'}, status=201)


@csrf_exempt
@login_required
def invoice(request):

    # check if the user made the entry (check-in)
    is_guest = Guests.objects.filter(guest=request.user).exists()

    if is_guest:

        guest = Guests.objects.get(guest=request.user)
        guest_booking = guest.booking
        consumptions = Consumptions.objects.filter(user=request.user, booking=guest.booking).order_by('-date')

        paginator = Paginator(consumptions, 16) # Show 16 consumptions per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "hotel/invoice.html", {'page_obj': page_obj, 'is_guest': is_guest, 'guest_booking': guest_booking})

    else:

        return render(request, "hotel/invoice.html", {'is_guest': is_guest})


@csrf_exempt
@login_required
def messages(request):

    # when user visit messages, mark unreaded messages as readed
    adminhotel = User.objects.get(username='adminhotel')
    Messages.objects.filter(user=adminhotel, addressee=request.user).filter(state='u').update(state='r')

    messages = Messages.objects.filter(Q(user=request.user) | Q(addressee=request.user)).order_by('-date')
    paginator = Paginator(messages, 10) # Show 10 messages per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hotel/messages.html", {'page_obj': page_obj})


@csrf_exempt
@login_required
def sendmessage(request):

    data = json.loads(request.body)
    message_content = data.get("message_content","")
    # all messages are for the hotel management 
    addressee = User.objects.get(username='adminhotel')

    try:
        new_message = Messages(user=request.user,
                               addressee = addressee,
                               message = message_content)
        new_message.save()
    except IntegrityError:
        return JsonResponse({'message': 'Error in send message.'}, status=401)
    return JsonResponse({'message': 'Successful message.'}, status=201)


@csrf_exempt
@login_required
def deletemessage(request):

    data = json.loads(request.body)
    message_id = data.get("message_id","")
 
    query = Messages.objects.filter(id=message_id).delete()

    # test if delete was successful 
    if query[0] > 0:
        return JsonResponse({'message': 'Message deleted.'}, status=201)
    else:
        return JsonResponse({'message': 'Error: Message has already been deleted.'}, status=400)


@csrf_exempt
@login_required
def unreadmessages(request):

    adminhotel = User.objects.get(username='adminhotel')
    unreaded = Messages.objects.filter(user=adminhotel, addressee=request.user).filter(state='u').count()

    return JsonResponse({'unreaded': unreaded})

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

        if (single_available < 0):
            single_available = 0
        
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

        if (double_available < 0):
            double_available = 0


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

        if (triple_available < 0):
            triple_available = 0

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

        if (quadruple_available < 0):
            quadruple_available = 0

        # ranges of rooms availables by type to pass to the selects in booking.html
        single_range = range(0, single_available + 1)
        double_range = range(0, double_available + 1)
        triple_range = range(0, triple_available + 1)
        quadruple_range = range(0, quadruple_available + 1)

        return render(request, "hotel/bookings.html", { 'check_in_date': checkInDate,
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


@login_required
@csrf_exempt
def mybookings(request):

    today = date.today()

    bookings = Bookings.objects.filter(user=request.user).order_by('checkin_date')
    is_guest = Guests.objects.filter(guest=request.user).exists()

    if request.method != "POST":
        post = False
        error = False
        return  render(request, "hotel/mybookings.html", { 'post': post, 
                                                           'error': error,
                                                           'bookings': bookings,
                                                           'today': today,
                                                           'is_guest': is_guest })

    if request.method == "POST":
        user_booking_post = request.POST["user_booking"]
        singles_booking = int(request.POST["singles_booking"])
        doubles_booking = int(request.POST["doubles_booking"])
        triples_booking = int(request.POST["triples_booking"])
        quadruples_booking = int(request.POST["quadruples_booking"])
        datein_booking = request.POST["datein_booking"]
        dateout_booking = request.POST["dateout_booking"]
        code_booking = request.POST["code_booking"]
        amount_booking_prov = request.POST["amount_booking"]

        if (amount_booking_prov != None):
            amount_booking = float(amount_booking_prov)
        else:
            amount_booking = 0
    
        empty_rooms = singles_booking + doubles_booking + triples_booking + quadruples_booking

        if (empty_rooms < 1):
            post = False    
            error = True
            return render(request, "hotel/mybookings.html", { 'message': 'No rooms selected.',
                                                              'post': post,
                                                              'error': error,
                                                              'bookings': bookings,
                                                              'today': today,
                                                              'is_guest': is_guest })

        if (amount_booking <= 0):
            post = False    
            error = True
            return render(request, "hotel/mybookings.html", { 'message': 'Your reservation amount could not be calculated, please try again later.',
                                                              'post': post,
                                                              'error': error,
                                                              'bookings': bookings,
                                                              'today': today,
                                                              'is_guest': is_guest })

        if ( datein_booking is None):
            post = False    
            error = True
            return render(request, "hotel/mybookings.html", { 'message': 'Empty Check-In or Check-Out dates.',
                                                              'post': post,
                                                              'error': error,
                                                              'bookings': bookings,
                                                              'today': today,
                                                              'is_guest': is_guest })

        if (code_booking is None):
            post = False    
            error = True
            return render(request, "hotel/mybookings.html", { 'message': 'No code of check-out availabe, try again later.',
                                                              'post': post,
                                                              'error': error,
                                                              'bookings': bookings,
                                                              'today': today,
                                                              'is_guest': is_guest })

        user_booking = User.objects.get(id=user_booking_post)

        # Prevent Duplicate Post
        duplicate = Bookings.objects.filter(checkout_code=code_booking).exists()

        if (duplicate == False):
        # Create & Save Booking
            booking = Bookings( user= user_booking,
                                singles= singles_booking,
                                doubles= doubles_booking,
                                triples= triples_booking,
                                quadruples= quadruples_booking,
                                checkin_date= datein_booking,
                                checkout_date= dateout_booking,
                                checkout_code= code_booking,
                                amount= amount_booking_prov )

            booking.save()
        
            post = True
            error = False
            return render(request, "hotel/mybookings.html", { 'singles_booking': singles_booking,
                                                              'doubles_booking': doubles_booking,
                                                              'triples_booking': triples_booking,
                                                              'quadruples_booking': quadruples_booking,
                                                              'datein_booking': datein_booking,
                                                              'dateout_booking': dateout_booking,
                                                              'amount_booking': amount_booking,
                                                              'post': post,
                                                              'error': error,
                                                              'bookings': bookings,
                                                              'today': today,
                                                              'is_guest': is_guest })
    
        else:
            post = False
            error = True
            return render(request, "hotel/mybookings.html", { 'message': 'Booking has already been saved.',
                                                              'post': post,
                                                              'error': error,
                                                              'bookings': bookings,
                                                              'today': today })


def facilities(request):
    
    return render(request, "hotel/facilities.html")


def houserules(request):
    
    return render(request, "hotel/houserules.html")


def finalprint(request):
    
    return render(request, "hotel/finalprint.html")


def reviews(request):

        name_color = ['Red','Blue','Green','Orange','BlueViolet','Brown',
                      'Chocolate','Coral','DarkOliveGreen','DarkSalmon',
                      'FireBrick','DodgerBlue','GoldenRod','OrangeRed']

        comments = Comments.objects.all().order_by('-date')

        average_calc = Comments.objects.aggregate(Avg('score'))
        average = round(average_calc['score__avg'], 1)
        reviews = Comments.objects.all().count()


        paginator = Paginator(comments, 8) # Show 8 comments per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "hotel/reviews.html", { 'page_obj': page_obj, 
                                                       'name_color': name_color,
                                                       'average': average,
                                                       'reviews': reviews })


def faqs(request):
    
    return render(request, "hotel/faqs.html")


@csrf_exempt
def language(request):

    user_language = request.POST["language"]
    translation.activate(user_language)  
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

    return render(request, "hotel/index.html")


@csrf_exempt
@login_required
def deletebooking(request):

    if request.method != "POST":
        return JsonResponse({'message': 'Error: POST request required.'}, status=400)

    data = json.loads(request.body)
    booking_to_delete_id = data.get("bookingtodelete","")
    
    query = Bookings.objects.filter(id=booking_to_delete_id).delete()

    # test if delete was successful 
    if query[0] > 0:
        return JsonResponse({'message': 'Booking deleted.'}, status=201)
    else:
        return JsonResponse({'message': 'Error: Booking has already been deleted.'}, status=400)


@csrf_exempt
@login_required
def checkinbooking(request):

    if request.method != "POST":
        return JsonResponse({'message': 'Error: POST request required.'}, status=400)

    try: 
        data = json.loads(request.body)
        booking_to_checkin_id = data.get("bookingtocheckin","")
    
        booking_to_checkin = Bookings.objects.get(id=booking_to_checkin_id)
        booking_to_checkin.checkin = True
        booking_to_checkin.save()

        guest=Guests(guest=request.user, booking=booking_to_checkin)
        guest.save()

        rooms_service = Services.objects.get(description='Rooms')

        first_consumption = Consumptions(user=request.user,
                                         booking= booking_to_checkin,
                                         service= rooms_service,
                                         date = date.today(),
                                         quantity = 1,
                                         amount = booking_to_checkin.amount)
        first_consumption.save()

    except IntegrityError:
        return JsonResponse({'message': 'Error: the check in process could not be done.'}, status=401)    

    lenguaje = request.LANGUAGE_CODE
        
    if lenguaje == 'en':
         message_content = 'Welcome to the hotel Le Monde, thank you for choosing us.'
    if lenguaje == 'es':
        message_content = 'Bienvenido al hotel Le Monde, gracias por elegirnos.'
    if lenguaje == 'pt':
        message_content = 'Bem vindo ao hotel Le Monde, obrigado por nos escolher.'

    adminhotel = User.objects.get(username='adminhotel')

    new_message = Messages(user= adminhotel,
                           addressee = request.user,
                           message = message_content)
    new_message.save()
        
    return JsonResponse({'message': 'Check In Successed.'}, status=201)


@csrf_exempt
@login_required
def checkoutbooking(request):

    data = json.loads(request.body)
    booking_to_checkout = data.get("bookingid","")
    # code_of_checkout = data.get("code","")
    comment = data.get("comment","")
    score = int(data.get("score",""))

    booking_checkout = Bookings.objects.get(id=booking_to_checkout)
    # To facilitate testing, code verification was bypassed
    # but the script for its validation is as follows
    
    # if (booking_checkout.checkout_code != code_of_checkout):
    #    return JsonResponse({'message': 'Error: checkout code invalid.'}, status=401)
   

    # remove user from Guests
    try:
        Guests.objects.filter(guest=request.user).filter(booking=booking_checkout).delete()

    except IntegrityError:
        return JsonResponse({'message': 'Error in delete user from Guests.'}, status=401)


    # remove consumptions from Consumptions (assumed that they are paid, that is validated with the exit code)
    try:
        Consumptions.objects.filter(user=request.user).filter(booking=booking_checkout).delete()
    except IntegrityError:
        return JsonResponse({'message': 'Error: in delete consumptions from Consumtions.'}, status=401)

    if ((len(comment) > 0) and (score > 0)):
         try:
            new_comment = Comments(user = request.user,
                                   date = date.today(),
                                   comment = comment,
                                   score = score)

            new_comment.save()

         except IntegrityError:
             return JsonResponse({'message': 'Error: in save your review in Comments.'}, status=401)


    # delete booking
    try:
        booking_checkout.delete()
    except IntegrityError:
        return JsonResponse({'message': 'Error: the booking could not be deleted.'}, status=401)

    return JsonResponse({'message': 'Successful Checkout.'}, status=201)


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
                'message': 'Invalid username and/or password.'
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
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hotel/register.html")
