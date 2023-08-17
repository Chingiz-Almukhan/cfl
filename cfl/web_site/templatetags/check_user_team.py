import datetime

from django import template
from pytz import timezone

from web_site.models import Membership, Challenge

register = template.Library()


@register.filter(name='has_team_and_captain')
def has_team_and_captain(user):
    return Membership.objects.filter(user=user, role='captain').exists()


@register.filter(name='has_team')
def has_team(user):
    return Membership.objects.filter(user=user).exists()


@register.filter(name='my_challenge')
def my_challenge(user, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    return challenge.first_team.members.filter(pk=user.pk).exists()


@register.filter(name='our_challenge')
def our_challenge(user, challenge_id):
    challenge = Challenge.objects.get(pk=challenge_id)
    return challenge.first_team.members.filter(pk=user.pk).exists() or challenge.second_team.members.filter(
        pk=user.pk).exists()


@register.filter(name='tz')
def timezone_reverse(value, timezone_name):
    local_tz = timezone('UTC')
    value_with_tz = local_tz.localize(datetime.datetime.combine(datetime.datetime.now().date(), value), is_dst=None)
    target_tz = timezone(timezone_name)
    target_time = value_with_tz.astimezone(target_tz).time()
    return target_time
