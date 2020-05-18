from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from apps.base.models import BaseModel


class UserPosition(BaseModel):
    name = models.CharField(max_length=256, unique=True)
    short_name = models.CharField(max_length=128)

    class Meta:
        db_table = 'user_position'


class UserTeam(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField()
    leader = models.CharField(max_length=150)

    class Meta:
        db_table = 'user_team'


class UserProjectJoined(BaseModel):
    MAX_TEAM_SIZE = 50

    name = models.CharField(max_length=256, unique=True)
    short_name = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()
    project_leader = models.CharField(max_length=150)
    members = ArrayField(models.CharField(max_length=10, blank=True), size=MAX_TEAM_SIZE)

    class Meta:
        db_table = 'user_project_joined'


class User(AbstractBaseUser, BaseModel):
    ROLE_ADMIN = 0
    ROLE_MEMBER = 1
    USER_ROLES = (
        (ROLE_ADMIN, 'Sun Admin'),
        (ROLE_MEMBER, 'Sun Member'),
    )

    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    role = models.IntegerField(choices=USER_ROLES, default=ROLE_MEMBER)
    is_activate = models.BooleanField(default=False)
    position = models.ForeignKey(UserPosition, on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(UserTeam, on_delete=models.CASCADE, null=True)
    user_project_joined = models.ManyToManyField(UserProjectJoined, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return 'User: {}'.format(self.username)


class UserSkill(BaseModel):
    LEVELS = (
        (0, 'Junior'),
        (1, 'Middle 1'),
        (2, 'Middle 2'),
        (3, 'Senior'),
    )
    name = models.CharField(max_length=128)
    level = models.IntegerField(choices=LEVELS, default=LEVELS[0][0])
    years_experience = models.IntegerField(default=1)
    user = models.ManyToManyField(User)

    class Meta:
        db_table = 'user_skill'
