"""View functions for yahrzeit app."""

import json
from typing import Union
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from yahrzeit_app import helpers
from yahrzeit_app import crud


def index(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """Render homepage."""

    logged_in = request.user.is_authenticated

    today = helpers.today_date_string()

    context = {
        'js_key': helpers.js_key,
        'today': today,
        'logged_in': logged_in,
    }

    return render(request, 'index.html', context)


def create_account_form(request: HttpRequest) -> Union[
    HttpResponse,
    HttpResponseRedirect,
]:
    """Render create account form."""

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'create_account.html')


def do_create_account(request: HttpRequest) -> JsonResponse:
    """API endpoint that performs checks and saves new account to database if checks pass."""

    request_data = json.loads(request.body)
    email = request_data['email']
    password = request_data['password']

    user = crud.create_user(email, password)

    if user:
        messages.add_message(
            request,
            messages.INFO,
            'Account successfully created',
        )
        login(request, user=user)

        result = request.session.get('result')

        if result and result['status'] == 'active':
            crud.create_decedent(
                user,
                result['decedent_name'],
                result['death_date_h'],
                result['next_date_h'],
                result['next_date_g'],
            )
            del request.session['result']

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failure'})


def login_form(request: HttpRequest) -> Union[
    HttpResponse,
    HttpResponseRedirect,
]:
    """Render login form."""

    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'login.html')


def do_login(request: HttpRequest) -> HttpResponseRedirect:
    """Perform checks and log user in if checks pass."""

    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)

    if user:
        login(request, user=user)

        crud.update_decedents_for_user(user)

        result = request.session.get('result')

        if result and result['status'] == 'active':
            crud.create_decedent(
                user,
                result['decedent_name'],
                result['death_date_h'],
                result['next_date_h'],
                result['next_date_g'],
            )
            del request.session['result']

        return redirect('dashboard')

    messages.add_message(
        request,
        messages.INFO,
        'Incorrect username or password',
    )

    return redirect('login_form')


def do_logout(request: HttpRequest) -> HttpResponseRedirect:
    """Log current user out."""

    logout(request)

    return redirect('index')


@login_required
def dashboard(request: HttpRequest) -> Union[
    HttpResponse,
    HttpResponseRedirect,
]:
    """Render user dashboard."""

    decedents = crud.get_decedents_for_user(request.user)

    context = {
        'decedents': decedents,
    }

    return render(request, 'dashboard.html', context)


def calculate(request: HttpRequest) -> HttpResponse:
    """Calculate next yahrzeit date."""
    # TODO Should this be GET since we're not writing to database?

    decedent_name = request.POST['decedent-name']
    decedent_date = request.POST['decedent-date']

    sunset = request.POST['TOD']
    after_sunset = False if sunset == 'before-sunset' else True

    num_years = int(request.POST['number'])

    next_date_h, next_date_g, is_it_today = helpers.get_next_date(
        decedent_date,
        after_sunset,
    )

    following_dates = helpers.get_following_dates(next_date_h, num_years-1)

    next_date_h_db = helpers.h_date_stringify_db(next_date_h)
    next_date_g_db = helpers.g_date_stringify_db(next_date_g)

    result_for_sesh = {
        'decedent_name': decedent_name,
        'death_date_h': helpers.greg_to_heb(decedent_date),
        'next_date_h': next_date_h_db,
        'next_date_g': next_date_g_db,
        'status': 'dormant',
    }

    request.session['result'] = result_for_sesh

    next_date_h_res = helpers.h_date_stringify_res(next_date_h)
    next_date_g_res = helpers.g_date_stringify_res(next_date_g)

    template_context = {
        'logged_in': True if request.user.is_authenticated else False,
        'next_date_h': next_date_h_res,
        'next_date_g': next_date_g_res,
        'following_dates': following_dates,
        'is_it_today': is_it_today,
        'decedent_name': decedent_name,
    }

    return render(request, 'result.html', template_context)


def save_res(request: HttpRequest) -> JsonResponse:
    """API endpoint that saves a calculation result for a logged in user."""

    result = request.session.get('result')

    if not result or not request.user.is_authenticated:
        return JsonResponse({'status': 'failure'})

    crud.create_decedent(
        request.user,
        result['decedent_name'],
        helpers.greg_to_heb(result['death_date_h']),
        result['next_date_h'],
        result['next_date_g'],
    )

    return JsonResponse({'status': 'success'})


def activate_res(request: HttpRequest) -> JsonResponse:
    """API endpoint to activate result for saving upon creation of account or login."""

    result = request.session.get('result')

    if not result:
        return JsonResponse({'status': 'failure'})

    result['status'] = 'active'
    request.session.modified = True

    return JsonResponse({'status': 'success'})


def get_sunset_time(request: HttpRequest, date_string, location_string) -> JsonResponse:
    """API endpoint that returns JSON data of sunset time for given day."""

    sunset_time = helpers.get_sunset_time(date_string, location_string)

    return JsonResponse({'sunset_time': sunset_time})
