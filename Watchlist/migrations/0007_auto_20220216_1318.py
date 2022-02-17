# Generated by Django 3.2.9 on 2022-02-16 13:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Watchlist', '0006_watchlist_last_watched'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='last_watched',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]