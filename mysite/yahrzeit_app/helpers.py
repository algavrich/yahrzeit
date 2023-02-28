"""Helper module for Yahrzeit app."""

from datetime import datetime, date
import os
from typing import Tuple, Dict
from astral import LocationInfo, sun
from pyluach import dates, hebrewcal
import googlemaps

gmaps_key = os.environ['GMAPS_KEY']
js_key = os.environ['JS_KEY']


def date_from_string(date_string: str) -> datetime.date:
    """Parse a date object from a string."""

    return datetime.strptime(date_string, '%Y-%m-%d').date()

#converting a gregorian string to a hebrew string
def greg_to_heb(greg_str):
    #parse date
    #convert to hebrew date obj
    return h_date_stringify_db(
        dates.HebrewDate.from_pydate(
            date_from_string(greg_str)
        )
    )

#hebrew date has a month and day. we need to find occurance of next month and day. What is curr year
def get_next_date(date_string:str, after_sunset: bool) -> Tuple:
    date_as_date = date_from_string(date_string)
    #instantiate a gregorian date with our values
    #instead of calling it on the hebrew instance we call it on the hebrew class itself
    hebrew_date = dates.HebrewDate.from_pydate(date_as_date)
    print(hebrew_date)
    print(after_sunset)
    if after_sunset:
        hebrew_date = hebrew_date.add(days=1)
    print(hebrew_date)
    future_month = hebrew_date.month
    #use .to_heb() on our gregorian date
    # get hebrew date of today - HebrewDate.today()
    today_h = dates.HebrewDate.today()
    # if hebrew_date was leap month and this year doesn't have leap, make it month 12
    if (hebrewcal.Year(hebrew_date.year).leap
        and not hebrewcal.Year(today_h).leap):
        future_month = 12
        
    this_h_year_yahr = dates.HebrewDate(
        today_h.year,
        future_month,
        hebrew_date.day,
    )

    # yahrziet hasn't passed yet this year
    if today_h < this_h_year_yahr:
        next_date_h = this_h_year_yahr
        next_date_g = next_date_h.to_greg()
        is_it_today = False
    # yahrzeit has already passed for this year
    elif today_h > this_h_year_yahr:
        next_date_h = dates.HebrewDate(
            today_h.year + 1,
            hebrew_date.month,
            hebrew_date.day,
        )
        next_date_g = next_date_h.to_greg()
        is_it_today = False
    # yahrzeit is today
    else:
        next_date_h = dates.HebrewDate(
            today_h.year + 1,
            hebrew_date.month,
            hebrew_date.day,
        )
        next_date_g = next_date_h.to_greg()
        is_it_today = True

    return (next_date_h, next_date_g, is_it_today)


def h_date_stringify_res(hebrew_date: dates.HebrewDate) -> str:
    """Format Hebrew date as a string for result."""

    return f'{hebrew_date:%-d %B} {hebrew_date.year}'


def g_date_stringify_res(gregorian_date: dates.GregorianDate) -> str:
    """Format Gregorian date as a string for result."""

    return f'{gregorian_date:%-d %B %Y}'


def h_date_stringify_db(hebrew_date: dates.HebrewDate) -> str:
    """Format Hebrew date as a string for database."""

    return f'{hebrew_date:%Y-%m-%d}'


def g_date_stringify_db(gregorian_date: dates.GregorianDate) -> date:
    """Format Gregorian date as a string for storage in session."""

    return f'{gregorian_date:%Y-%m-%d}'


def get_following_dates(
        next_date_h: dates.HebrewDate,
        num_years: int,
    ) -> Dict:
    """Return dictionary of hebrew and gregorian dates for specified number
    of future years.

    """

    #create empty dict for dates
    following_dates = {}

    #iterate the number of times for the number of years requested
    for num in range(1, num_years+1):
        #within each iteration, add that number to the year - hebrew
        following_date_h = dates.HebrewDate(
            next_date_h.year+num,
            next_date_h.month,
            next_date_h.day,
        )
        #convert date to gregorian
        following_date_g = following_date_h.to_greg()

        #turn dates to strings and add to dict
        following_dates[
            h_date_stringify_res(following_date_h)
        ] = g_date_stringify_res(following_date_g)

    #return dict
    return following_dates


def geocode_address(location: str) -> list:
    """Geocode an address."""

    gmaps = googlemaps.Client(key=gmaps_key)

    return gmaps.geocode(location)


def get_timezone(coordinates: tuple) -> str:
    """Get timezone from address."""

    gmaps = googlemaps.Client(key=gmaps_key)

    return gmaps.timezone(coordinates)


def get_sunset_time_helper(
        date_string: str,
        location_string: str,
    ) -> datetime.time:
    """Get time of sunset on given day at given location."""

    location_data = geocode_address(location_string)
    coordinates = location_data[0]['geometry']['location']
    location_name = location_data[0]['address_components'][0]['long_name']
    location_region = location_data[0]['address_components'][-1]['long_name']
    tz = get_timezone(coordinates)['timeZoneId']

    location = LocationInfo(
        location_name,
        location_region,
        tz,
        coordinates['lat'],
        coordinates['lng'],
    )
    try:
        sunset = sun.sunset(
            location.observer,
            date_from_string(date_string),
            tz,
        )
    except ValueError:
        return

    return (date.strftime(sunset, '%-I:%M %p'))