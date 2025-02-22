from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """
    User Management Mixin
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def buyers(self):
        return self.filter(type=User.TypeChoices.BUYER)

    def shops(self):
        return self.filter(type=User.TypeChoices.SHOP)

class User(AbstractUser):
    """
    Standard user model
    """
    class TypeChoices(models.TextChoices):
        SHOP = 'shop', 'Shop'
        BUYER = 'buyer', 'Buyer'

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True)
    company = models.CharField(max_length=40, blank=True)
    position = models.CharField(max_length=40, blank=True)
    type = models.CharField(verbose_name='User type', choices=TypeChoices.choices, max_length=5, default=TypeChoices.BUYER)
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"
        ordering = ('email',)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'



