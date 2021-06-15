# CS50 - Capstone - Final Project - Hotel Web
## Table of contents
- [Introduction](#introduction)
  * [Description](#description)
  * [Installation](#installation)
  * [Usage-tips](#use)
- [Implementation](#implementation)
  * [Models](#models)
    + [User](#user)
    + [Guests](#guests)
    + [Room](#room)
    + [Bookings](#bookings)
    + [Services](#services)
    + [Consumptions](#consumptions)
    + [Comments](#comments)
    + [Messages](#messages)
  * [Views](#views)
    + [bookings](#bookings)
    + [facilities](#facilities)
    + [faqs](#faqs)
    + [houserules](#houserules)
    + [info](#info)
    + [invoice](#invoice)
    + [language](#language)
    + [loginview](#loginview)
    + [logoutview](#logoutview)
    + [messages](#messages)
    + [mybookings](#mybookings)
    + [orders](#orders)
    + [register](#register)
    + [reviews](#like)
  * [API-Views](#api-views)
    + [deletebooking](#deletebooking)
    + [checkinbooking](#checkinbooking)
    + [checkoutbooking](#checkoutbooking)
    + [makeanorder](#makeanorder)
    + [sendmessage](#sendmessage)
    + [deletemessage](#deletemessage)
    + [unreadmessages](#unreadmessages)
  * [Files](#files)
- [Screenshots](#screenshots)


# Introduction
## Description

A web application was developed for a fictitious Hotel. In this application the hotel provides information
about its characteristics and services. The user can check for available rooms, specifying a range of dates,
and make the corresponding reservation (to do this, the user must first register).
The user can self-manage their Check-in and Check-out.

During the stay at the hotel, the user can place orders at the hotel reception, and exchange messages.
The amount of the user's reservation, and the consumptions made, are added to an expense invoice, 
that can also be consulted at any time. 

The site has been developed for three different languages (English, Spanish and Portuguese),
which can be changed by the user at any time. 
 
Hotel guests can leave a comment and rating when checking out.
 

## Distinctiveness and Complexity

The most outstanding characteristics and other that make it different from the other projects of the course are: 

     1. Extensive use of Bootstrap
     2. Photo gallery
     3. Multilanguage
     4. Full mobile-responsive in all pages
     5. Eight Django Models
     6. Messaging system
     7. Ordering system to the front-desk
     8. Detail of consumption made
     9. Check available rooms
    10. Make reservations
    11. Guest review statistics

With the functionalities implemented in points points 6 to 11, it can be seen that the complexity of the system
is greater than the other projects, however, it is in the description of the views, where the complexity
of the complete system will be appreciated, since each process will be detailed there.

For this reason, I recommend reading all the descriptions of the processes that are made in the views, to understand the characteristics that make this system different.


## Installation

To set up this project on your computer:

    1. Download the project
    2. Install all Python packages listed in requirements.txt
        a. apt install gettext (for linux system)
    3. Be sure to use the supplied database, as it contains information necessary for the correct  
     operation of the system.

The system was tested with Django 3.1.5 and Django 3.2


## Usage tips  

For test like admin or front-desk user, use 'adminhotel' as username and 'abc123' as password.  


# Implememtation

## Models

### User
Contains: Django Abstract User

### Guests
Contains: the list of Users who have Checked-in.  
Fields:
* guest (user)
* booking (reservation)

### Room
Contains: the description of the room (single, double, etc.), the type code, the amount the hotel has of them, and the rate per night.  
Fields:
* description
* roomtype
* quantity
* rate

### Bookings
Contains: the user who made it, the number of rooms reserved for each type, the dates of entry and exit, the total amount of consumption and and the status of checkin (true when guest did Check-in).  
Fields:
* user
* singles
* doubles
* triples
* quadruples
* checkin_date
* checkout_date
* checkout_code
* amount
* checkin

### Services
Contains: the description of the service, the confirmation message, or instructions received by the guest and the service fee.  
Fields:
* description
* description_es
* description_pt
* message
* message_es
* message_pt
* rate

### Consumptions
Contains: saves each consumption of products or services that the guest makes.  
Fields:
* user
* booking
* service (description)
* date
* quantity

### Comments
Contains: the guest, date, review, and the score.  
Fields:
* user
* date
* comment (review)
* score (1 to 5)

### Messages
Contains: the sender, the date and and time, the recipient, content and state (read or unread).  
Fields:
* user
* date
* addressee
* message
* state

## Views

### Bookings  

It allows you to check the availability of rooms, for this you must indicate the desired arrival and departure dates, the query returns the number of rooms available for each type, for the indicated dates. The room types are Single, Double, Triple and Quadruple.  

If the user is logged in, he can make the reservation, otherwise he can only see the availability of rooms. The system informs the number of nights chosen, and the cost; which changes as the rooms are chosen.  

At the booking, the total amount for the rooms is saved, since room rates may vary.

Uses USER, BOOKINGS and ROOM models. Works in conjunction with the code contained in bookings.js.


### Facilities  

It is a static page, which informs which are the main facilities and services of the hotel.


### FAQs  

It is a static page, which answers the most frequent questions from users. Works in conjunction with the code contained in faqs.js.  


### Houserules  

Is a static page that contains important information about the hotel's rules about Check-in or Check-out times, pets, accepted cards, etc.  


### Info  

Contains the hotel presentation and a photo gallery. Works in conjunction with the code contained in slideshow.js.  


### Invoice  

Available if the user is logged in. It shows the user a list of the consumptions of their current booking and the total amount owed. 
It will be without information if the user did not Check-in. Use the CONSUMPTIONS model.


### Language  

Supervises the language chosen by the user.  


### Loguinview  

Manage user login. Use the USER model.


### Logoutview  

Manage user logout. Use the USER model.  


### Messages  

Available if the user is logged in. It shows the user his message history with the hotel administration. Also, can reply and delete them. A notification appears if there are unread messages. Works in conjunction with the code contained in messages.js. Use the MESSAGES model.  


### Mybookings  

Available if the user is logged in. Shows all bookings user, or reports that it has none. Works in conjunction with the code contained in mybookings.js.   

It should not be confused with the "Bookings" view, which is for making a reservation or inquiring about room availability.  

If the user has a reservation, he can do three things:

    1. Delete it (enabled only if the Check-in was not done).
    2. Check-in (it is enabled when the system date coincides with the reservation date).
    3. Check-out.  

When the Check-in is done:
  * The first charge or consumption is generated, which is that of the rooms (CONSUMPTIONS model).  
  * Only the option to do the Check-out is available.  
  * The user is added to the hotel's guest list (GUESTS model).  
  * The booking status is marked as entered (checkin = true) in BOOKINGS model.  

Only one reservation at a time can be in Check-in status.

When the Check-out is done:  

  * Consumptions are erased (CONSUMPTIONS model).
  * The user is removed from the guests list (GUESTS model).
  * The booking is deleted (BOOKINGS model).
  * the guest can leave a comment -only chance- (COMMENTS model).

To check out, a code that the hotel administration would provide to the guest at the time of making the payment of their consumptions is necessary. This feature is stopped, in order to facilitate the use and demonstration of the system. It is implemented, but its code is commented.  


### Orders  

Available if the user is logged. Here are the services that the guest has at their disposal and the price (SERVICES model). He can request them (if he did the Check-in), and the amount of the consumption is added to his account (CONSUMPTIONS model); and to the total in his booking (BOOKINGS model).   

For each request made by the guest, a message is left in their mailbox, with instructions or additional information.

Works in conjunction with the code contained in orders.js  


### Register  

Manages user registration. Use the USER model.  


### Reviews  

This section shows the hotel reviews (COMMENTS model), comments also have a score which is averaged and displayed at the top of the page.  


## API-Views  

### Deletebooking  

Receives the identification of the booking to be deleted, performs the operation (BOOKINGS model), and returns the result.  


### Checkinbooking   

Receives the identification of the booking that makes the entry, adds the user to the guest list (GUESTS model), and the amount of the rooms to consumption (CONSUMPTIONS model).


### Checkoutbooking  

Receives the identification of the booking that makes the Check-out, deletes the user from the guest list (GUESTS model), delete the consumptions corresponding to that reservation (CONSUMPTIONS model), delete the booking (BOOKINGS model); if the user leaves a review, it is saved (COMMENTS model).  


### Makeanorder  

Receives the order ID and the requested quantity, add the amount of consumption to the total of the booking (BOOKINGS model), the administration sends the guest a message confirming receipt of the order and a message with the order details is sent to the hotel administration (MESSAGES model), finally, add the consumption to the bill (CONSUMPTIONS model).  


### Sendmessage

Receives the content to be sent in a message to the hotel front-desk and processes it (MESSAGES model).  


### Deletemessage  

Receives the ID of the message to be deleted and proceeds (MESSAGES model).  


### Unreadmessages  

Monitor the amount of unread messages the current user has (MESSAGES model).  


## Files  

  * /locale/es/django.po (Spanish translations).
  * /locale/pt/django.po (Portuguese translations).
  * /static/hotel/bookings.js (JavaScript code for the bookings.html page).
  * /static/hotel/common.js (JavaScript code for all pages).
  * /static/hotel/faqs.js (JavaScript code for faqs.html page).
  * /static/hotel/messages.js (JavaScript code for messages.html page).
  * /static/hotel/mybookings.js (JavaScript code for mybookings.html page).
  * /static/hotel/orders.js (JavaScript code for orders.html page).
  * /static/hotel/slideshow.js (JavaScript for image gallery in index.html page).
  * /static/hotel/styles.css (CSS styles).
  * /static/hotel/icons (icons for index.html and houserules.html pages).
  * /static/hotel/images (images for gallery in index.html).
  * /static/hotel/screenshots (screenshots of the app).
  * /templates/hotel/bookings.html (implements Bookings view).
  * /templates/hotel/facilities.html (implements Facilities view).
  * /templates/hotel/faqs.html (implements Faqs view).
  * /templates/hotel/houserules.html (implements Houserules view).
  * /templates/hotel/index.html (implements Info view).
  * /templates/hotel/invoice.html (implements Invoice view).
  * /templates/hotel/layout.html (layout template for all html pages).
  * /templates/hotel/login.html (implements Login view).
  * /templates/hotel/messages.html (implements Messages view).
  * /templates/hotel/mybookings.html (implements Mybookings view).
  * /templates/hotel/orders.html (implementes Orders view).
  * /templates/hotel/register.html (implements Register view).
  * /templates/hotel/reviews.html (implements Reviews view).
  * /hotel/models.py (contains the definition of all data models).
  * /hotel/views.py (contains all views).
  * /hotel/db.sqlite3 (database).
  * /hotel/README.md (this file).
  * /hotel/requirements.txt (list of packages that need to be installed).  


# Screenshots
 

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel01.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel02.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel03.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel04.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel05.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel06.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel07.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel08.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel09.png?raw=true)

![alt text](https://github.com/me50/pablocourault/blob/web50/projects/2020/x/capstone/hotel/static/screenshots/hotel10.png?raw=true)













