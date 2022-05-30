# Generated by Django 3.1.3 on 2022-05-16 20:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_registration_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(blank=True, max_length=4000, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=4000, null=True)),
                ('town', models.CharField(blank=True, max_length=4000, null=True)),
                ('postcode', models.CharField(blank=True, max_length=4000, null=True)),
                ('country', models.CharField(blank=True, choices=[('BELARUS', 'Беларусь'), ('UKRAINE', 'Украина'), ('POLAND', 'Польша'), ('UK', 'Великобритания'), ('FINLAND', 'Финляндия')], max_length=15, null=True)),
                ('address_zone', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название жилого помещения')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание жилого помещения')),
                ('type', models.CharField(choices=[('HOTEL', 'Отель'), ('APARTMENT', 'Квартира'), ('HOUSE', 'Дом'), ('HOSTEL', 'Хостел'), ('COTTAGE', 'Коттедж')], max_length=15, verbose_name='Тип жилого помещения')),
                ('rooms_qty', models.IntegerField(verbose_name='Количество комнат')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Цена за день проживания')),
                ('add_date', models.DateField(default=datetime.datetime(2022, 5, 16, 20, 10, 37, 271440, tzinfo=utc), verbose_name='Дата добавления')),
                ('rating', models.FloatField(null=True, verbose_name='Оценка жилого помещения')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property', to='reservation_app.address')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='login_registration_app.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True, verbose_name='Уникальный идентификатор удобсва')),
                ('img', models.ImageField(upload_to='facility_icons/', verbose_name='Иконка')),
                ('name', models.CharField(max_length=15, verbose_name='Название удобсва')),
                ('properties', models.ManyToManyField(related_name='services', to='reservation_app.Property', verbose_name='Помещение с удобством')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
                ('kids_qty', models.PositiveIntegerField(verbose_name='Количество детей')),
                ('adults_qty', models.PositiveIntegerField(verbose_name='Количество взрослых')),
                ('booked_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservation_app.property', verbose_name='Забронированное помещение')),
                ('resident_who_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='login_registration_app.resident', verbose_name='Человек, который забронировал помещение')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_images/')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='reservation_app.property')),
            ],
        ),
    ]