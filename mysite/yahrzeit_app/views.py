"""View functions for yahrzeit app."""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from yahrzeit_app import helpers
from yahrzeit_app import crud

#home - intro and form to calculate yahrzeit date
def index(request):
    """Render homepage."""
    
    if request.session.get('user_id'):
        return redirect('dashboard')

    return render(request, 'index.html')

#create account
def create_account_form(request):
    """Render create account form."""

    return render(request, 'create_account.html')


def create_account(request):
    """Perform checks and save new account to database if checks pass."""

    email = request.POST['email']
    password = request.POST['password']

    if crud.create_user(email, password):
        # Flash success
        messages.add_message(
            request,
            messages.INFO,
            'Account successfully created',
        )
    else:
        # Flash not success
        messages.add_message(
            request,
            messages.INFO,
            'That email is already asssociated with an account',
        )

    return redirect('index')


#login
def login_form(request):
    """Render login form."""

    if request.session.get('user_id'):
        return redirect('dashboard')

    return render(request, 'login.html')


def login(request):
    """Perform checks and log user in if checks pass."""

    email = request.POST['email']
    password = request.POST['password']

    user = crud.get_user_by_email(email)

    if user and user.check_password(password):
        #Log user in, redirect to dashboard
        request.session['user_id'] = user.pk
        messages.add_message(
            request,
            messages.INFO,
            'Logged in successfully',
        )

        return redirect('dashboard')
    else:
        #Redirect to index, flash either username or password incorrect
        messages.add_message(
            request,
            messages.INFO,
            'Incorrect username or password',
        )
        return redirect('index')


#user dashboard - list of decedents and dates, option to add a decedent, option to recieve email reminders
def dashboard(request):
    """Render user dashboard."""

    if not request.session.get('user_id'):
        return redirect('index')

    return HttpResponse('This is the dashboard.')

#calculate
def calculate(request):
    """Calculate next yahrzeit date."""
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