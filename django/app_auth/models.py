from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
import os, uuid
from django.dispatch import receiver
from django.db.models.signals import post_save

import braintree


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    # filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    filename = f"{instance.username}-{uuid.uuid4()}"[:50] + f".{ext}"
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)

class User(AbstractUser):

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

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
