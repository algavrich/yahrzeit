"""Helper module for Yahrzeit app."""

from pyluach import dates
from datetime import datetime

def get_next_date(date_string:str):
    date_as_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    #instantiate a gregorian date with our values
    #instead of calling it on the hebrew instance we call it on the hebrew class itself
    hebrew_date = dates.HebrewDate.from_pydate(date_as_date)
    #use .to_heb() on our gregorian date
    print(hebrew_date)
