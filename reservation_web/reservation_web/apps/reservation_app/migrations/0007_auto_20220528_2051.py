# Generated by Django 3.1.3 on 2022-05-28 17:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0006_auto_20220526_2256'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AddField(
            model_name='service',
            name='is_search_service',
            field=models.BooleanField(default=False, verbose_name='Удобство используется при поиске?'),
        ),
        migrations.AlterField(
            model_name='property',
            name='add_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 28, 17, 51, 46, 226245, tzinfo=utc), verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='from_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='to_date',
            field=models.DateField(),
        ),
    ]