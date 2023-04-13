"""Helper module for Yahrzeit app."""

from datetime import datetime, date
import os
from typing import Tuple, Dict, Union
from astral import LocationInfo, sun
from pyluach import dates, hebrewcal
import googlemaps

gmaps_key = os.environ['GMAPS_KEY']
js_key = os.environ['JS_KEY']


def date_from_string(date_string: str) -> datetime.date:
    """Parse a date object from a string."""

    return datetime.strptime(date_string, '%Y-%m-%d').date()


def greg_to_heb(greg_str: str) -> str:
    """Convert gregorian date string to hebrew date string."""

    return h_date_stringify_db(
        dates.HebrewDate.from_pydate(
            date_from_string(greg_str),
        )
    )


def adjust_adar_leap(month: int, year: int) -> int:
    """Return yahrzeit month adjusted for future year's leap status."""

    if (month == 13 and not hebrewcal.Year(year).leap):
        return 12

    return month


def today_date_string() -> str:
    """Return string of today's date."""

    return date.strftime(date.today(), '%Y-%m-%d')


def get_next_date(date_string: str, after_sunset: bool = False) -> Tuple:
    """Calculate next yahrzeit date."""

    date_as_date = date_from_string(date_string)
    hebrew_date = dates.HebrewDate.from_pydate(date_as_date)

    if after_sunset:
        hebrew_date = hebrew_date.add(days=1)

    today_h = dates.HebrewDate.today()

    this_h_year_yahr = dates.HebrewDate(
        today_h.year,
        adjust_adar_leap(hebrew_date.month, today_h.year),
        hebrew_date.day,
    )

    if today_h < this_h_year_yahr:
        next_date_h = this_h_year_yahr
        next_date_g = next_date_h.to_greg()
        is_it_today = False

    else:
        next_date_h = dates.HebrewDate(
            today_h.year + 1,
            adjust_adar_leap(hebrew_date.month, today_h.year+1),
            hebrew_date.day,
        )
        next_date_g = next_date_h.to_greg()

        if today_h > this_h_year_yahr:
            is_it_today = False

        else:
            is_it_today = True

    return (next_date_h, next_date_g, is_it_today)


def h_date_stringify_res(hebrew_date: dates.HebrewDate) -> str:
    """Format Hebrew date as a string for result."""

    return f'{hebrew_date:%-d %B %Y}'


def g_date_stringify_res(gregorian_date: dates.GregorianDate) -> str:
    """Format Gregorian date as a string for result."""

    return f'{gregorian_date:%-d %B %Y}'


def h_date_stringify_db(hebrew_date: dates.HebrewDate) -> str:
    """Format Hebrew date as a string for database."""

    return f'{hebrew_date:%Y-%m-%d}'


def g_date_stringify_db(gregorian_date: dates.GregorianDate) -> date:
    """Format Gregorian date as a string for storage in session."""

    return f'{gregorian_date:%Y-%m-%d}'


def h_date_db_to_res(h_date_str: str) -> str:
    """Format Hebrew date string (from DB) for dashboard."""

    date_parts = [int(x) for x in h_date_str.split('-')]
    h_date = dates.HebrewDate(date_parts[0], date_parts[1], date_parts[2])
    return h_date_stringify_res(h_date)


def g_date_db_to_res(g_date_str: str) -> str:
    """Format Hebrew date string (from DB) for dashboard."""

    date_parts = [int(x) for x in g_date_str.split('-')]
    g_date = dates.GregorianDate(date_parts[0], date_parts[1], date_parts[2])
    return g_date_stringify_res(g_date)


def get_following_dates(
    next_date_h: dates.HebrewDate,
    num_years: int,
) -> Dict:
    """Return dictionary of hebrew and gregorian dates for specified number
    of future years.

    """

    following_dates = {}

    for num in range(1, num_years+1):
        following_date_h = dates.HebrewDate(
            next_date_h.year+num,
            adjust_adar_leap(next_date_h.month, next_date_h.year+num),
            next_date_h.day,
        )
        following_date_g = following_date_h.to_greg()

        following_dates[
            h_date_stringify_res(following_date_h)
        ] = g_date_stringify_res(following_date_g)

    return following_dates


def geocode_address(location: str) -> list:
    """Geocode an address."""

    gmaps = googlemaps.Client(key=gmaps_key)

    return gmaps.geocode(location)


def get_timezone(coordinates: tuple) -> str:
    """Get timezone from address."""

    gmaps = googlemaps.Client(key=gmaps_key)

    return gmaps.timezone(coordinates)


def get_sunset_time(
    date_string: str,
    location_string: str,
) -> Union[str, None]:
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

    return (datetime.strftime(sunset, '%-I:%M %p'))
