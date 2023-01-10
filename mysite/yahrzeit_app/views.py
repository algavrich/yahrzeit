from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render

#home - intro and form to calculate yahrzeit date
def index(request):
    return render(request, 'index.html')
#create account
def create_account(request):
    return HttpResponse('This is create account page.')
#login
#user dashboard - list of decedents and dates, option to add a decedent, option to recieve email reminders