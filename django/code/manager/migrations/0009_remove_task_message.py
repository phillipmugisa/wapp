# Generated by Django 4.1.5 on 2023-03-01 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_task_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='message',
        ),
    ]
