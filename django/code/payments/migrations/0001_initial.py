# Generated by Django 4.1.5 on 2023-01-28 13:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BraintreePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.CharField(default='0', max_length=256, verbose_name='Plan Id')),
                ('name', models.CharField(default='0', max_length=256, verbose_name='name')),
                ('description', models.TextField(default='0', verbose_name='description')),
                ('billing_frequency', models.CharField(default='0', max_length=256, verbose_name='billing_frequency')),
                ('currency_iso_code', models.CharField(default='0', max_length=256, verbose_name='currency_iso_code')),
                ('Price', models.CharField(default='0', max_length=256, verbose_name='Price')),
            ],
        ),
        migrations.CreateModel(
            name='PaypalPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='Paypal ID')),
                ('name', models.CharField(max_length=256, verbose_name='Plan Name')),
                ('status', models.CharField(default='ACTIVE', max_length=256, verbose_name='Plan status')),
                ('currency', models.CharField(max_length=256, verbose_name='Plan Currency')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Plan Cost')),
                ('description', models.TextField(max_length=256, verbose_name='Description')),
                ('interval_unit', models.CharField(max_length=256, verbose_name='Plan Duration')),
                ('interval_count', models.IntegerField(default=1, verbose_name='Interval Count')),
                ('subscribers', models.IntegerField(default=0, verbose_name='Plan Subscribers')),
            ],
        ),
        migrations.CreateModel(
            name='PaypalProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, max_length=256, null=True, verbose_name='Product Id')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('ProductType', models.CharField(default='Service', max_length=256, verbose_name='Type')),
                ('description', models.TextField(max_length=256, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='PaypalSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(default=datetime.date.today, verbose_name='Created on')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paypalplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='paypalplan',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.paypalproduct'),
        ),
        migrations.CreateModel(
            name='features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('plan', models.ManyToManyField(related_name='pricing_feature', to='payments.paypalplan')),
            ],
        ),
        migrations.CreateModel(
            name='BraintreeSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(default=datetime.date.today, verbose_name='Created on')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.braintreeplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]