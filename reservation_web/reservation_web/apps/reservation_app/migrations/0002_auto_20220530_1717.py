# Generated by Django 3.1.3 on 2022-05-30 14:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='price_for_booking',
            field=models.IntegerField(default=0, verbose_name='Плата за бронирование'),
        ),
        migrations.AlterField(
            model_name='property',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 30, 14, 17, 45, 929923, tzinfo=utc), verbose_name='Дата добавления'),
        ),
    ]