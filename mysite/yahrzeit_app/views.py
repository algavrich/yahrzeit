from django.shortcuts import render, redirect
from django.http import HttpResponse
from yahrzeit_app import helpers
from yahrzeit_app import crud

#home - intro and form to calculate yahrzeit date
def index(request):
    """Render homepage."""
    return render(request, 'index.html')
#create account
def create_account_form(request):
    """Render create account form."""
    return render(request, 'create_account.html')

def create_account(request):
    """Perform checks and save new account to database if checks pass."""
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    if crud.create_user(username, email, password):
        # Flash success
        pass
    else:
        # Flash not success
        pass

    return redirect('index')
#login
#user dashboard - list of decedents and dates, option to add a decedent, option to recieve email reminders
#calculate
def calculate(request):
    #TODO Should this be get since we're not writing to database?
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

    next_date_h, next_date_g, is_it_today = helpers.get_next_date(decedent_date)
    
    return HttpResponse(str(next_date_h) + str(next_date_g), str(is_it_today))