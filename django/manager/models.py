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


# id: Math.random() * 50,
# name: template_name,
# color: template_color,
# message: template_extension_message,
# date_created: `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`,
class Template(models.Model):
    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=256, blank=True, null=True)
    template_id = models.CharField(_("template_id"), max_length=256, blank=True, null=True)
    color = models.CharField(_("Color"), max_length=256, blank=True, null=True)
    message = models.TextField(_("message"))
    date_created = models.CharField(_("date_created"), max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

# _task["inEdit"] = True;
# _task["name"] = msg_name;
# _task["contact"] = selected_contact;
# _task["color"] = msg_color;
# _task["template"] = saved_template;
# _task["sending_date"] = schedule_date;
# _task["sending_time"] = schedule_time;
# _task["date_created"] = `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`;


class Task(models.Model):
    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=256, blank=True, null=True)
    color = models.CharField(_("Color"), max_length=256, blank=True, null=True)
    contact = models.CharField(_("contact"), max_length=256, blank=True, null=True)
    template = models.CharField(_("template_id"), max_length=256, blank=True, null=True)

    sending_date = models.CharField(_("sending_date"), max_length=256, blank=True, null=True)
    sending_time = models.CharField(_("sending_time"), max_length=256, blank=True, null=True)

    date_created = models.CharField(_("date_created"), max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

# id: Math.random() * 50,
# name: memo_name,
# description: memo_description,
# color: memo_color,
# date_created: `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`,

class Memo(models.Model):
    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=256, blank=True, null=True)
    color = models.CharField(_("Color"), max_length=256, blank=True, null=True)
    description = models.TextField(_("description"))
    date_created = models.CharField(_("date_created"), max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

class Alarm(models.Model):
    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_("Name"), max_length=256, blank=True, null=True)
    color = models.CharField(_("Color"), max_length=256, blank=True, null=True)
    display_area = models.CharField(_("Display Area"), max_length=256, blank=True, null=True)
    template = models.CharField(_("template_id"), max_length=256, blank=True, null=True)

    alarm_date = models.CharField(_("alarm_date"), max_length=256, blank=True, null=True)
    alarm_time = models.CharField(_("alarm_time"), max_length=256, blank=True, null=True)

    date_created = models.CharField(_("date_created"), max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

class BlockedSite(models.Model):
    user = models.ForeignKey(to=AuthModels.User, on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField(_("url"), max_length=256, blank=True, null=True)
    date_created = models.CharField(_("date_created"), max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.url}"