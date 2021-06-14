# CS50 - Capstone - Final Project - Hotel Web
## Table of contents
- [Introduction](#introduction)
  * [Description](#description)
  * [Installation](#installation)
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
    + [index](#index)
    + [bookings](#post-comment)
    + [facilities](#user-profile)
    + [houserules](#edit-profile)
    + [reviews](#like)
    + [faqs](#following)
    + [orders](#follow-unfollow)
    + [invoice](#login-view)
    + [messages](#logout-view)
    + [mybookings](#register)
  * [API-Views](#api-views)
-[Files](#Files)
- [Screenshots](#screenshots)


# Introduction
## Description

A web application was developed for a fictitious Hotel. In this application the hotel provides information
about its characteristics and services. The user can check for available rooms, specifying a range of dates,
and make the corresponding reservation (to do this, the user must first register).
The user can self-manage their check-in and check-out.

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
    3. Be sure to use the supplied database, as it contains information necessary for the correct operation of the system.

The system was tested with Django 3.1.5 and Django 3.2


# Implememtation

## Models

### User
Contains: Django Abstract User

### Guests
Contains: the list of Users who have checked-in. 
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
Contains: the user who made it, the number of rooms reserved for each type, the dates of entry and exit, the total amount of consumption and and the status of checkin (true when guest did check in).
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




