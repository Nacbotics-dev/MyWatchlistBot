# Generated by Django 3.2.9 on 2022-02-14 00:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('chat_id', models.CharField(max_length=120, null=True)),
                ('user_name', models.CharField(blank=True, editable=False, max_length=120, null=True)),
                ('user_id', models.CharField(editable=False, max_length=120, primary_key=True, serialize=False)),
                ('date_joined', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('movie_id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True)),
                ('movie_title', models.CharField(max_length=120)),
                ('watched', models.BooleanField(default=True)),
                ('update_url', models.URLField(blank=True)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='Watchlist.user')),
            ],
        ),
    ]
