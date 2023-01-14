"""CRUD module for yahrzeit app."""

from yahrzeit_app.models import User


def create_user(username: str, password: str, email: str) -> bool:
    """Instantiate a User with given attributes and save to database."""

    if not get_user_by_email(email) and not get_user_by_username(username):
        new_user = User(username=username, password=password, email=email)
        new_user.save()
        return True
    else:
        return False


def get_user_by_email(email:str) -> User:
    """Retrieve a User with given email if it exists.
    Otherwise, return None.
    
    """

    return User.objects.filter(email=email).first()


def get_user_by_username(username:str) -> User:
    """Retrieve a User with given username if it exists.
    Otherwise, return None.
    
    """

    return User.objects.filter(username=username).first()

