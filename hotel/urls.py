from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("language", views.language, name="set_language"),
    path("info", views.index, name="info"),
    path("bookings", views.bookings, name="bookings"),
    path("facilities", views.facilities, name="facilities"),
    path("houserules", views.houserules, name="houserules"),
    path("finalprint", views.finalprint, name="finalprint"),
    path("guestsreviews", views.guestsreviews, name="guestsreviews"),
    path("faqs", views.faqs, name="faqs"),      
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('i18n/', include('django.conf.urls.i18n')),
    path("mybookings", views.mybookings, name="mybookings"),
    # API Routes
    path("deletebooking", views.deletebooking, name="deletebooking"),

]

