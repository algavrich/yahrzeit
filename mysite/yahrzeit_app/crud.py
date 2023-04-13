"""CRUD module for yahrzeit app."""

from django.db.models import QuerySet
from yahrzeit_app.models import CustomUser, Decedent
from yahrzeit_app.helpers import (
    today_date_string,
    get_next_date,
    h_date_db_to_res,
    g_date_db_to_res,
)


def create_user(email: str, password: str) -> bool:
    """Instantiate a User with given attributes and save to database."""

    if not get_user_by_email(email):
        return CustomUser.objects.create_user(email, password)


def get_user_by_email(email: str) -> CustomUser:
    """Retrieve a User with given email if it exists.
    Otherwise, return None.

    """

    return CustomUser.objects.filter(email=email).first()


def create_decedent(user: CustomUser, name: str, death_date_hebrew: str,
                    next_date_hebrew: str, next_date_gregorian: str) -> None:
    """Instantiate a Decedent with given attributes and save to database."""

    new_decedent = Decedent(
        user=user,
        name=name,
        death_date_hebrew=death_date_hebrew,
        next_date_hebrew=next_date_hebrew,
        next_date_gregorian=next_date_gregorian,
    )
    new_decedent.save()


def get_decedents_for_user(user: CustomUser) -> QuerySet:
    """Retrieve a list of Decedents for given user."""

    decedents = Decedent.objects.filter(
        user=user,
    )
    decedents = {
        decedent.name: ' / '.join([
            h_date_db_to_res(decedent.next_date_hebrew),
            g_date_db_to_res(decedent.next_date_gregorian),
        ])
        for decedent in decedents
    }

    return decedents


def update_decedents_for_user(user: CustomUser) -> None:
    """Update related decedent records for a user."""

    needs_update = Decedent.objects.filter(
        user=user.pk,
        next_date_gregorian__lt=today_date_string(),
    )

    for decedent in needs_update:
        next_date_data = get_next_date(decedent.next_date_gregorian)
        decedent.next_date_hebrew = next_date_data[0]
        decedent.next_date_gregorian = next_date_data[1]
        decedent.save()
