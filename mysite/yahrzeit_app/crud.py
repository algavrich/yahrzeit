"""CRUD module for yahrzeit app."""

from yahrzeit_app.models import User, Decedent


def create_user(email: str, password: str) -> bool:
    """Instantiate a User with given attributes and save to database."""

    if not get_user_by_email(email):
        new_user = User(password=password, email=email)
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

def get_decedents_for_user(user_id):
    """Retrieve a list of Decedents for given user."""

    return Decedent.objects.filter(
        user=get_user_by_id(user_id),
    )