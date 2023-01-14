from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-account-form', views.create_account_form, name='create_account_form'),
    path('create-account', views.create_account, name='create_account'),
    path('calculate', views.calculate, name='calculate'),
]