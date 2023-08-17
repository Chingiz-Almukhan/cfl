# Generated by Django 4.1.7 on 2023-03-11 21:54

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
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_owner', models.BooleanField(default=False)),
                ('is_invited', models.BooleanField(default=False)),
                ('role', models.CharField(blank=True, choices=[('captain', 'captain'), ('member', 'member')], max_length=20, null=True, verbose_name='User role')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_team', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Participants in team',
                'verbose_name_plural': 'Participants in teams',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Team name')),
                ('max_members', models.PositiveIntegerField(blank=True, default=5, null=True)),
                ('min_members', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('members', models.ManyToManyField(related_name='team_members', through='web_site.Membership', to=settings.AUTH_USER_MODEL, verbose_name='participants')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_i_play', to='web_site.team'),
        ),
        migrations.CreateModel(
            name='Ladder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Ladder name')),
                ('rules', models.TextField(verbose_name='Rules')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                ('teams', models.ManyToManyField(related_name='ladder_team', to='web_site.team', verbose_name='Teams')),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('active', 'active'), ('dispute', 'dispute'), ('finished', 'finished')], default='active', max_length=20, null=True, verbose_name='Challenge status')),
                ('result_first_team', models.CharField(blank=True, choices=[('won', 'won'), ('loss', 'loss')], max_length=20, null=True, verbose_name='Report first team')),
                ('result_second_team', models.CharField(blank=True, choices=[('won', 'won'), ('loss', 'loss')], max_length=20, null=True, verbose_name='Report second team')),
                ('proof_first_team', models.CharField(blank=True, max_length=20, null=True, verbose_name='Proof')),
                ('proof_second_team', models.CharField(blank=True, max_length=20, null=True, verbose_name='Proof')),
                ('first_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_team', to='web_site.team', verbose_name='first team')),
                ('second_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_team', to='web_site.team', verbose_name='second team')),
            ],
        ),
    ]
