"""CRUD module for yahrzeit app."""

from yahrzeit_app.models import User


def create_user(email: str, password: str) -> bool:
    """Instantiate a User with given attributes and save to database."""

    if not get_user_by_email(email):
        new_user = User(password=password, email=email)
        new_user.save()
        return True
    else:
        return False


def safe_get(func):
    """Decorator to handle DoesNotExist exceptions for queries."""

    def wrapper_safe_get(*args, **kwargs):
        """Wrapper to handle DoesNotExist exceptions for queries."""

        try:
            return func(*args, **kwargs)
        except User.DoesNotExist:
            return None

    return wrapper_safe_get


@safe_get
def get_user_by_email(email:str) -> User:
    """Retrieve a User with given email if it exists.
    Otherwise, return None.
    
    """

    return User.objects.filter(email=email).first()

    
