"""Helper module for Yahrzeit app."""

from pyluach import dates
from datetime import datetime, date

#converting a gregorian string to a hebrew string
def greg_to_heb(greg_str):
    #parse date
    #convert to hebrew date obj
    return h_date_stringify_db(
        dates.HebrewDate.from_pydate(
            datetime.strptime(greg_str, '%Y-%m-%d').date()
        )
    )

#hebrew date has a month and day. we need to find occurance of next month and day. What is curr year
def get_next_date(date_string:str):
    date_as_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    #instantiate a gregorian date with our values
    #instead of calling it on the hebrew instance we call it on the hebrew class itself
    hebrew_date = dates.HebrewDate.from_pydate(date_as_date)
    #use .to_heb() on our gregorian date
    # get hebrew date of today - HebrewDate.today()
    today_h = dates.HebrewDate.today()
    this_h_year_yahr = dates.HebrewDate(today_h.year, hebrew_date.month, hebrew_date.day)

    # yahrziet hasn't passed yet this year
    if today_h < this_h_year_yahr:
        next_date_h = this_h_year_yahr
        next_date_g = next_date_h.to_greg()
        is_it_today = False
    # yahrzeit has already passed for this year
    elif today_h > this_h_year_yahr:
        next_date_h = dates.HebrewDate(today_h.year + 1, hebrew_date.month, hebrew_date.day)
        next_date_g = next_date_h.to_greg()
        is_it_today = False
    # yahrzeit is today
    else:
        next_date_h = dates.HebrewDate(today_h.year + 1, hebrew_date.month, hebrew_date.day)
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
    ):
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