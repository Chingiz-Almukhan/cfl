# Generated by Django 4.1.7 on 2023-04-18 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0007_team_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='is_captain',
            field=models.BooleanField(default=False),
        ),
    ]
