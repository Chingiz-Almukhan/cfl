from accounts.managers import AccountManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True, blank=False)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatars',
        verbose_name='avatar',
    )
    email_verify = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=40, null=True, blank=True)
    username = models.CharField(verbose_name='username', unique=True, null=False, blank=False, max_length=25)
    psn = models.CharField(verbose_name='psn', unique=True, null=False, blank=False, max_length=25, default='psn')
    timezone = models.CharField(verbose_name='timezone', null=True, blank=True, max_length=50)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.username}'
