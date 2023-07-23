from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
import os, uuid
from django.dispatch import receiver
from django.db.models.signals import post_save

import braintree


from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Try to find the user using the email field instead of the username field
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If the user is not found, return None (i.e., authentication failed)
            return None
        else:
            # Check the password and return the user if it's correct
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    # filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    filename = f"{instance.username}-{uuid.uuid4()}"[:50] + f".{ext}"
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)

class User(AbstractBaseUser, PermissionsMixin):

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    email = models.EmailField('Email address', unique=True)
    country_code = models.CharField("Country Code", max_length=10, null=True, blank=True)
    phone_number = models.CharField("Phone Number", max_length=20, null=True, blank=True)
    is_email_activated = models.BooleanField("Email Activated", default=False)
    is_phone_activated = models.BooleanField("Phone Activated", default=False)
    profile_image = models.FileField(verbose_name="Profile Image",upload_to=get_file_path, null=True, blank=True)
    verify_code = models.CharField("Verification Code", max_length=10, null=True, blank=True)
    customer_payemnt_id = models.CharField("Customer Payment Id", max_length=256, null=True, blank=True)
    
    def get_moblie_number(self):
        return f"+{self.country_code}{self.phone_number[1:] if self.phone_number[0] == '0' else self.phone_number}"

    def str(self):
        return self.email
