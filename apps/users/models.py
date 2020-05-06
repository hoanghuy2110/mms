from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.db import models

from apps.base.models import BaseModel


class User(AbstractBaseUser, BaseModel):
    ROLE_ADMIN = 0
    ROLE_MEMBER = 1
    USER_ROLES = (
        (ROLE_ADMIN, 'Sun Admin'),
        (ROLE_MEMBER, 'Sun Member'),
    )

    username = models.CharField(_('username'), max_length=150)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=ROLE_MEMBER)
    is_activate = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'User: {}'.format(self.username)
