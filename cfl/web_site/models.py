from django.db import models


class Team(models.Model):
    name = models.CharField(verbose_name='Team name', max_length=20, unique=True)
    members = models.ManyToManyField(
        to='accounts.Account',
        through='web_site.Membership',
        verbose_name='participants',
        related_name='team_members',
    )
    points = models.PositiveIntegerField(null=True, blank=True, default=1000)
    max_members = models.PositiveIntegerField(null=True, blank=True, default=5)
    min_members = models.PositiveIntegerField(null=True, blank=True, default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'


USER_ROLE = (
    ('captain', 'captain'),
    ('member', 'member'),
)


class Membership(models.Model):
    user = models.ForeignKey(to='accounts.Account', on_delete=models.CASCADE, related_name='team_i_play')
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE, related_name='participant_team')
    is_owner = models.BooleanField(default=False)
    is_invited = models.BooleanField(default=False)
    is_captain = models.BooleanField(default=False)
    role = models.CharField(
        verbose_name='User role',
        max_length=20,
        choices=USER_ROLE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Participants in team'
        verbose_name_plural = 'Participants in teams'


CHALLENGE_STATUS = (
    ('active', 'active'),
    ('waiting_result', 'waiting_result'),
    ('dispute', 'dispute'),
    ('finished', 'finished')
)
CHALLENGE_RESULT = (
    ('won', 'won'),
    ('loss', 'loss'),
)


class Maps(models.Model):
    name = models.CharField(verbose_name='Map_name', max_length=20, unique=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)


class Challenge(models.Model):
    first_team = models.ForeignKey(to=Team, verbose_name='first team', on_delete=models.CASCADE,
                                   related_name='first_team')
    second_team = models.ForeignKey(to=Team, verbose_name='second team', on_delete=models.CASCADE,
                                    related_name='second_team', null=True, blank=True)
    first_map = models.ForeignKey(to=Maps, verbose_name='first_map', related_name="first_map", null=True, blank=True,
                                  on_delete=models.CASCADE)
    second_map = models.ForeignKey(to=Maps, verbose_name='second_map', related_name="second_map", null=True, blank=True,
                                   on_delete=models.CASCADE)
    third_map = models.ForeignKey(to=Maps, verbose_name='third_map', related_name="third_map", null=True, blank=True,
                                  on_delete=models.CASCADE)
    time_start = models.TimeField(auto_now_add=True)
    modified = models.TimeField(auto_now=True)
    status = models.CharField(
        verbose_name='Challenge status',
        max_length=20,
        choices=CHALLENGE_STATUS,
        null=True,
        blank=True,
        default='active'
    )
    result_first_team = models.CharField(
        verbose_name='Report first team',
        max_length=20,
        choices=CHALLENGE_RESULT,
        null=True,
        blank=True,
    )
    result_second_team = models.CharField(
        verbose_name='Report second team',
        max_length=20,
        choices=CHALLENGE_RESULT,
        null=True,
        blank=True,
    )
    proof_first_team = models.CharField(verbose_name='Proof', max_length=20, null=True, blank=True)
    proof_second_team = models.CharField(verbose_name='Proof', max_length=20, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Ladder(models.Model):
    name = models.CharField(verbose_name='Ladder name', max_length=50)
    rules = models.TextField(verbose_name='Rules')
    teams = models.ManyToManyField(
        to=Team,
        verbose_name='Teams',
        related_name='ladder_team',
    )
    end_date = models.DateTimeField(auto_now=False, verbose_name='End date')
