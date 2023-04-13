"""Models for yahrzeit app database."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Model for a UserManager."""

    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """Model for a User."""

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        """String representation for User."""

        return f"<User email={self.email}>"

    @property
    def is_staff(self):
        return self.is_admin


class Decedent(models.Model):
    """Model for a Decedent."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    death_date_hebrew = models.CharField(max_length=10)
    next_date_hebrew = models.CharField(max_length=10)
    next_date_gregorian = models.CharField(max_length=10)

    def __str__(self) -> str:
        """String representation for Decedent."""

        return f"<Decedent name={self.name}>"
