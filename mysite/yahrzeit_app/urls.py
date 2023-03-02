"""URL paths for yahrzeit app."""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(
        'create-account-form',
        views.create_account_form,
        name='create_account_form',
    ),
    path('create-account', views.create_account, name='create_account'),
    path('login-form', views.login_form, name='login_form'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('calculate', views.calculate, name='calculate'),
    path('dashboard', views.dashboard, name='dashboard'),
    path(
        'api/get-sunset-time/<str:date_string>/<str:location_string>',
        views.get_sunset_time,
        name='get_sunset_time',
    ),
]