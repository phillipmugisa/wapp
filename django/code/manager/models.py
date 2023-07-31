from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import datetime
import uuid
from app_auth import models as AuthModels

def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    # filename = "%s-%s.%s" % (instance.slug, uuid.uuid4(), ext)
    filename = f"{instance.slug}-{uuid.uuid4()}"[:50] + f".{ext}"
    return os.path.join(f"{instance.__class__.__name__}/images/", filename)

def generate_schedule_datetime(schedule_date, schedule_time):
    # Assuming schedule_date and schedule_time are in the format "YYYY-MM-DD" and "HH:MM" respectively
    date_format = "%Y-%m-%d %H:%M"
    schedule_datetime_str = f"{schedule_date} {schedule_time}"
    schedule_datetime = datetime.datetime.strptime(schedule_datetime_str, date_format)
    return schedule_datetime

class Task(models.Model):
    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE, blank=True, null=True)
    data = models.JSONField(_("message data"))
    # day_recurrence = models.CharField(_("day_recurrence"), max_length=256, blank=True, null=True)
    # day_recurrence_day = models.CharField(_("day_recurrence_day"), max_length=256, blank=True, null=True)
    # single_interval_period = models.CharField(_("single_interval_period"), max_length=256, blank=True, null=True)
    # bundle_msg_count = models.CharField(_("bundle_msg_count"), max_length=256, blank=True, null=True)
    # bundle_msg_interval = models.CharField(_("bundle_msg_interval"), max_length=256, blank=True, null=True)
    # schedule_time = models.CharField(_("schedule_time"), max_length=256, blank=True, null=True)
    # schedule_date = models.CharField(_("schedule_date"), max_length=256, blank=True, null=True)
    # message = models.CharField(_("message"), max_length=256, blank=True, null=True)
    # files
    # contacts

    schedule_date = models.DateTimeField(_("Schedule Date"), null=True, blank=True)
    sent = models.BooleanField(_("is sent"), default=False)

    

    def save(self, *args, **kwargs):
        if self.data["timing"]["schedule_date"] and self.data["timing"]["schedule_time"]:
            schedule_datetime = generate_schedule_datetime(self.data["timing"]["schedule_date"], self.data["timing"]["schedule_time"])
            self.schedule_date = schedule_datetime

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user}"