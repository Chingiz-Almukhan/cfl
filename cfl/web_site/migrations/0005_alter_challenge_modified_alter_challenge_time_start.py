# Generated by Django 4.1.7 on 2023-04-03 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0004_alter_challenge_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='modified',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='time_start',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
