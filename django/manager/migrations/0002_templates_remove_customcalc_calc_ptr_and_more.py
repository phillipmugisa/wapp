# Generated by Django 4.1.5 on 2023-02-14 10:46

from django.db import migrations, models
import django.utils.timezone
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('message', models.TextField(verbose_name='message')),
                ('file_name', models.FileField(blank=True, null=True, upload_to=manager.models.get_file_path, verbose_name='Image')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='Safe Url')),
            ],
        ),
        migrations.RemoveField(
            model_name='customcalc',
            name='calc_ptr',
        ),
        migrations.RemoveField(
            model_name='ebaycalc',
            name='calc_ptr',
        ),
        migrations.DeleteModel(
            name='AmazonCalc',
        ),
        migrations.DeleteModel(
            name='Calc',
        ),
        migrations.DeleteModel(
            name='CustomCalc',
        ),
        migrations.DeleteModel(
            name='EbayCalc',
        ),
    ]
