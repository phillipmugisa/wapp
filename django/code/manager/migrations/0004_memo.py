# Generated by Django 4.1.5 on 2023-02-28 22:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_task_template_delete_templates_task_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('color', models.CharField(max_length=256, verbose_name='Color')),
                ('description', models.TextField(verbose_name='description')),
                ('date_created', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
            ],
        ),
    ]