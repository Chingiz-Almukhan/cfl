# Generated by Django 4.1.7 on 2023-03-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='psn',
            field=models.CharField(default='psn', max_length=25, unique=True, verbose_name='psn'),
        ),
    ]
