from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.contrib.auth.models import Group
from emapp.role.models import UserRoleModel

LEVEL_CHOICES = [
    ('Village', 'Village'),
    ('Tehsil', 'Tehsil'),
    ('Block', 'Block'),
    ('District', 'District'),
    ('State', 'State'),
]

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """Create and saves a new user """
        if not username:
            raise ValueError('user name must be non empty')
        user = self.model(username=username.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """ Create and saves super user """
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using username """
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    readonly = models.BooleanField(default=False)
    language = models.CharField(max_length=255, default="English")
    email = models.EmailField(max_length = 254,blank=True)
    groups = models.ManyToManyField(Group,blank=True)
    phone = models.CharField(max_length=12, unique=True, blank=True)
    roleId = models.ForeignKey(UserRoleModel, on_delete=models.SET_NULL, blank=True,null=True)
    is_public = models.BooleanField(default=False)
    play_device = models.BooleanField(default=True)
    notification_token = models.CharField(max_length=30, blank=True)
    notification_tokens = models.JSONField(blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'