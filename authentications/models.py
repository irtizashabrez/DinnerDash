from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxLengthValidator, MinLengthValidator


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, display_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have Password')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.display_name = display_name
        user.full_name = full_name
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, full_name, display_name=None):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            display_name=display_name,
            is_staff=True,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, full_name, display_name=None):
        user = self.create_user(
            email,
            password=password,
            full_name=full_name,
            display_name=display_name,
            is_staff=True,
            is_admin=True,
        )

        user.save(using=self._db)
        return user


class MyUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email', unique=True, max_length=255)
    full_name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(
        validators=[MinLengthValidator(2), MaxLengthValidator(32)], max_length=32,
        blank=True, null=True
    )
    active = models.BooleanField(default=True) 
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    object = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_disply_name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user a admin member?"
        return self.active

    def is_superuser(self):
        "Is the user a superuser?"
        return self.superuser
