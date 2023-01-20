"""URL paths for yahrzeit app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-account-form', views.create_account_form, name='create_account_form'),
    path('create-account', views.create_account, name='create_account'),
    path('login-form', views.login_form, name='login_form'),
    path('login', views.login, name='login'),
    path('calculate', views.calculate, name='calculate'),
    path('dashboard', views.dashboard, name='dashboard'),
]