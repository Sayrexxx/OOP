# Generated by Django 4.2.4 on 2024-05-29 01:24

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('role', models.CharField(choices=[('administrator', 'administrator'), ('passenger', 'passenger')], default='passenger', max_length=20)),
                ('phone_number', models.CharField(max_length=13)),
                ('age', models.PositiveSmallIntegerField(default=30)),
                ('secret_key', models.CharField(default='', max_length=20)),
                ('user_ptr', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('origin_point', models.CharField(max_length=20)),
                ('destination_point', models.CharField(max_length=20)),
                ('departure_time', models.DateTimeField(default=datetime.datetime(2024, 6, 1, 1, 24, 19, 426966, tzinfo=datetime.timezone.utc))),
                ('arrival_time', models.DateTimeField(default=datetime.datetime(2024, 6, 1, 1, 24, 19, 426985, tzinfo=datetime.timezone.utc))),
                ('available_seats', models.PositiveSmallIntegerField()),
                ('price', models.FloatField()),
                ('passengers', models.ManyToManyField(related_name='flights', to='aviaSales.myuser')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.PositiveSmallIntegerField(default=1)),
                ('price', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('В обработке ', 'В обработке'), ('Принят', 'Принят'), ('Отменён', 'Отменён')], default='В обработке', max_length=20)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='aviaSales.flight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='aviaSales.myuser')),
            ],
        ),
    ]
