"""View functions for yahrzeit app."""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from yahrzeit_app import helpers
from yahrzeit_app import crud

#home - intro and form to calculate yahrzeit date
# TODO is request of type HttpRequest? (type hinting)
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
        messages.add_message(
            request,
            messages.INFO,
            'Account successfully created',
        )
        user = crud.get_user_by_email(email)
        # if result in session, write it to DB
        request.session["user_id"] = user.pk

        # request.session['result']['decedent_name']
        result = request.session.get('result')

        if result:
            crud.create_decedent(
                user,
                result['decedent_name'],
                result['death_date_h'],
                result['next_date_h'],
                result['next_date_g'],
            )
            del request.session['result']

        return redirect('dashboard')

    else:
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
        # If result in session, write to DB
        result = request.session.get('result')

        if result:
            crud.create_decedent(
                user,
                result['decedent_name'],
                result['death_date_h'],
                result['next_date_h'],
                result['next_date_g'],
            )
            del request.session['result']

        return redirect('dashboard')
    else:
        #Redirect to index, flash either username or password incorrect
        messages.add_message(
            request,
            messages.INFO,
            'Incorrect username or password',
        )
        return redirect('index')
    

def logout(request):
    """Log current user out."""

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('index')
    
    del request.session['user_id']

    return redirect('index')


#user dashboard - list of decedents and dates, option to add a decedent, option to recieve email reminders
def dashboard(request):
    """Render user dashboard."""

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('index')
    
    decedents = crud.get_decedents_for_user(user_id)
    print(decedents)

    context = {
        'decedents': decedents,
    }

    return render(request, 'dashboard.html', context)


#calculate
def calculate(request):
    """Calculate next yahrzeit date."""
    #TODO Should this be get since we're not writing to database?

    decedent_name = request.POST['decedent-name']
    decedent_date = request.POST['decedent-date']
    num_years = int(request.POST['number'])

    next_date_h, next_date_g, is_it_today = helpers.get_next_date(decedent_date)

    following_dates = helpers.get_following_dates(next_date_h, num_years-1)

    next_date_h_res = helpers.h_date_stringify_res(next_date_h)
    next_date_g_res = helpers.g_date_stringify_res(next_date_g)

    next_date_h_db = helpers.h_date_stringify_db(next_date_h)
    next_date_g_db = helpers.g_date_stringify_db(next_date_g)

    user_id = request.session.get('user_id')
    # if user in session
    if user_id:
        user = crud.get_user_by_id(user_id)
        # write to db
        crud.create_decedent(
            user,
            decedent_name,
            helpers.greg_to_heb(decedent_date),
            next_date_h_db,
            next_date_g_db,
        )
        # display new date on dashboard
        return redirect('dashboard')

    # else
    else:
        template_context = {
            'next_date_h': next_date_h_res,
            'next_date_g': next_date_g_res,
            'following_dates': following_dates,
            'is_it_today': is_it_today,
            'decedent_name': decedent_name,
        }

        result_for_sesh = {
            'decedent_name': decedent_name,
            'death_date_h': helpers.greg_to_heb(decedent_date),
            'next_date_h': next_date_h_db,
            'next_date_g': next_date_g_db,
        }

        request.session['result'] = result_for_sesh

        return render(request, 'result.html', template_context)
        # go to page that shows result and asks to login/create acct