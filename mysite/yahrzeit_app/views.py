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
#calculate
def calculate(request):
    decedent_name = request.POST['decedent-name']
    decedent_date = request.POST['decedent-date']
    # if user in session
    if request.session.get('user_id'):
        logged_in = True
        # write to db
        # display new date on dashboard
    # else
    else:
        logged_in = False
        # go to page that shows result and asks to login/create acct
    return render()