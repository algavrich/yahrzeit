"""View functions for yahrzeit app."""

import json
from typing import Union
from django.shortcuts import render, redirect
from django.contrib import messages
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

    if request.session.get('user_id'):
        return redirect('dashboard')

    today = helpers.today_date_string()
    
    context = {
        'js_key': helpers.js_key,
        'today': today,
    }

    return render(request, 'index.html', context)


def create_account_form(request: HttpRequest) -> Union[
    HttpResponse,
    HttpResponseRedirect,
]:
    """Render create account form."""

    if request.session.get('user_id'):
        return redirect('dashboard')

    return render(request, 'create_account.html')


def create_account(request: HttpRequest) -> JsonResponse:
    """API!!! Perform checks and save new account to database if checks pass."""

    request_data = json.loads(request.body)
    email = request_data['email']
    password = request_data['password']

    if crud.create_user(email, password):
        messages.add_message(
            request,
            messages.INFO,
            'Account successfully created',
        )
        user = crud.get_user_by_email(email)
        request.session["user_id"] = user.pk

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

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failure'})



def login_form(request: HttpRequest) -> Union[
    HttpResponse,
    HttpResponseRedirect,
]:
    """Render login form."""

    if request.session.get('user_id'):
        return redirect('dashboard')

    return render(request, 'login.html')


def login(request: HttpRequest) -> HttpResponseRedirect:
    """Perform checks and log user in if checks pass."""

    email = request.POST['email']
    password = request.POST['password']

    user = crud.get_user_by_email(email)

    if user and helpers.verify_password(user, password):
        request.session['user_id'] = user.pk
        messages.add_message(
            request,
            messages.INFO,
            'Logged in successfully',
        )

        crud.update_decedents_for_user(user)

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
            'Incorrect username or password',
        )

        return redirect('index')
    

def logout(request: HttpRequest) -> HttpResponseRedirect:
    """Log current user out."""

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('index')
    
    del request.session['user_id']

    return redirect('index')


def dashboard(request: HttpRequest) -> Union[
    HttpResponse,
    HttpResponseRedirect,
]:
    """Render user dashboard."""

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('index')
    
    decedents = crud.get_decedents_for_user(user_id)
    context = {
        'decedents': decedents,
    }

    return render(request, 'dashboard.html', context)


def calculate(request: HttpRequest) -> HttpResponse:
    """Calculate next yahrzeit date."""
    #TODO Should this be GET since we're not writing to database?

    decedent_name = request.POST['decedent-name']
    decedent_date = request.POST['decedent-date']

    sunset = request.POST['TOD']
    after_sunset = False if sunset == 'before-sunset' else True

    num_years = int(request.POST['number'])

    next_date_h, next_date_g, is_it_today = helpers.get_next_date(decedent_date, after_sunset)

    following_dates = helpers.get_following_dates(next_date_h, num_years-1)

    next_date_h_db = helpers.h_date_stringify_db(next_date_h)
    next_date_g_db = helpers.g_date_stringify_db(next_date_g)

    user_id = request.session.get('user_id')

    if user_id:
        user = crud.get_user_by_id(user_id)

        crud.create_decedent(
            user,
            decedent_name,
            helpers.greg_to_heb(decedent_date),
            next_date_h_db,
            next_date_g_db,
        )

    else:
        result_for_sesh = {
            'decedent_name': decedent_name,
            'death_date_h': helpers.greg_to_heb(decedent_date),
            'next_date_h': next_date_h_db,
            'next_date_g': next_date_g_db,
        }

        request.session['result'] = result_for_sesh

    next_date_h_res = helpers.h_date_stringify_res(next_date_h)
    next_date_g_res = helpers.g_date_stringify_res(next_date_g)
    
    template_context = {
        'next_date_h': next_date_h_res,
        'next_date_g': next_date_g_res,
        'following_dates': following_dates,
        'is_it_today': is_it_today,
        'decedent_name': decedent_name,
    }

    return render(request, 'result.html', template_context)


def get_sunset_time(request: HttpRequest, date_string, location_string) -> JsonResponse:
    """API endpoint that returns JSON data of sunset time for given day."""

    sunset_time = helpers.get_sunset_time_helper(date_string, location_string)
    
    return JsonResponse({'sunset_time': sunset_time})