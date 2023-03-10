"""CRUD module for yahrzeit app."""

from django.db.models import QuerySet
from yahrzeit_app.models import User, Decedent
from yahrzeit_app.helpers import (
    hash_password,
    today_date_string,
    get_next_date,
)


def create_user(email: str, password: str) -> bool:
    """Instantiate a User with given attributes and save to database."""

    if not get_user_by_email(email):
        new_user = User(password=hash_password(password), email=email)
        new_user.save()
        
        return True
    
    return False


def get_user_by_id(user_id: int) -> User:
    """Retrieve a User with given id."""

    return User.objects.filter(pk=user_id).first()


def get_user_by_email(email: str) -> User:
    """Retrieve a User with given email if it exists.
    Otherwise, return None.

    """

    return User.objects.filter(email=email).first()


def create_decedent(user: User, name: str, death_date_hebrew: str,
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


def get_decedents_for_user(user_id: int) -> QuerySet:
    """Retrieve a list of Decedents for given user."""

    return Decedent.objects.filter(
        user=get_user_by_id(user_id),
    )


def update_decedents_for_user(user: User) -> None:
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