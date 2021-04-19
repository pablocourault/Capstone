from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.language, name="set_language"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('i18n/', include('django.conf.urls.i18n')),
]