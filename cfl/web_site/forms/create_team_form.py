from django import forms
from django.contrib.auth import get_user_model

from web_site.models import Team


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


# class EditTeamForm(forms.ModelForm):
#     members = forms.ModelMultipleChoiceField(
#         queryset=get_user_model().objects.all(),
#         widget=forms.CheckboxSelectMultiple, required=True
#     )
#
#     class Meta:
#         model = Team
#         fields = ['name', 'members']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         team_participants = self.instance.participant_team.all()
#         self.fields['participants'].initial = team_participants
