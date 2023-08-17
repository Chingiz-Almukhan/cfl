import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from accounts.models import Account
from web_site.forms.create_team_form import AddTeamForm
from web_site.forms.invite_form import InviteForm
from web_site.models import Ladder, Team, Membership, Challenge, Maps
from web_site.services import update_teams_points


class LadderDetailView(DetailView):
    template_name = 'ladder.html'
    model = Ladder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ladder = self.object
        teams = ladder.teams.filter(is_deleted=False).order_by('-points')
        if self.request.user.is_authenticated:
            tzname = self.request.user.timezone
            if tzname:
                self.request.session['django_timezone'] = tzname
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
            context['timezone_name'] = self.request.user.timezone
        context['teams'] = teams
        context['create_team_form'] = AddTeamForm
        context['challenges'] = Challenge.objects.filter(status='active', is_deleted=False)
        context['active_challenges'] = Challenge.objects.exclude(status__in=['active', 'finished', 'dispute'])
        return context


class MakeTeamView(CreateView):
    model = Team
    form_class = AddTeamForm

    def post(self, request, *args, **kwargs):
        ladder = Ladder.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            new_team = form.save()
            new_team.members.add(request.user)
            membership = Membership.objects.get(team=new_team, user=request.user)
            membership.is_owner = True
            membership.role = 'captain'
            membership.save()
            ladder.teams.add(new_team)
        return redirect('ladder_detail', pk=ladder.pk)


class CreateChallengeView(View):
    def post(self, request, *args, **kwargs):
        ladder = Ladder.objects.get(pk=kwargs['pk'])
        status = 'active'
        time_start = timezone.now()
        if Membership.objects.filter(user=request.user).exists():
            user_membership = Membership.objects.get(user=request.user)
            team = user_membership.team
            active_challenge = Challenge.objects.filter(first_team=team, status='active').exists()
            if active_challenge or Membership.objects.filter(team=team).count() < 3:
                pass
            else:
                challenge = Challenge.objects.create(status=status, time_start=time_start, first_team=team)
                challenge.save()
        return redirect('ladder_detail', pk=ladder.pk)


class AcceptChallengeView(View):
    def post(self, request, *args, **kwargs):
        challenge = Challenge.objects.get(pk=kwargs['pk'])
        status = 'waiting_result'
        modified = timezone.now()
        if Membership.objects.filter(user=request.user).exists():
            user_membership = Membership.objects.get(user=request.user)
            team = user_membership.team
            active_challenge = Challenge.objects.filter(first_team=team, status='active').exists()
            if active_challenge:
                pass
            else:
                challenge.second_team = team
                challenge.modified = modified
                challenge.status = status
                maps = Maps.objects.filter(is_active=True).order_by('?')[:3]
                if maps:
                    challenge.first_map = maps[0]
                    challenge.second_map = maps[1]
                    challenge.third_map = maps[2]
                challenge.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteChallenge(DeleteView):
    model = Challenge
    success_url = reverse_lazy('ladders')

    def post(self, request, *args, **kwargs):
        challenge = self.get_object()
        challenge.is_deleted = True
        challenge.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', self.success_url))


class ChallengeDetailView(DetailView):
    model = Challenge
    context_object_name = "challenge"
    template_name = "challenge_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_team = self.object.first_team
        memberships_first_team = first_team.participant_team.all()
        second_team = self.object.second_team
        memberships_second_team = second_team.participant_team.all()
        context['first_team'] = memberships_first_team
        context['second_team'] = memberships_second_team
        return context


class ReportChallengeView(UpdateView):
    model = Challenge

    def post(self, request, *args, **kwargs):
        challenge_object = self.get_object()
        result_first_team = request.POST.get('first_team', None)
        result_second_team = request.POST.get('second_team', None)
        if result_first_team:
            challenge_object.result_first_team = result_first_team
        if result_second_team:
            challenge_object.result_second_team = result_second_team
        challenge_object.save()
        if challenge_object.result_first_team and challenge_object.result_second_team:
            if challenge_object.result_first_team == "won" and challenge_object.result_second_team == "won" or \
                    challenge_object.result_first_team == "loss" and challenge_object.result_second_team == "loss":
                challenge_object.status = "dispute"
            else:
                team_one = Team.objects.get(pk=challenge_object.first_team.pk)
                team_two = Team.objects.get(pk=challenge_object.second_team.pk)

                if challenge_object.result_first_team == "won" and challenge_object.result_second_team == "loss":
                    update_teams_points(team_one, team_two)
                    challenge_object.status = "finished"
                elif challenge_object.result_first_team == "loss" and challenge_object.result_second_team == "won":
                    update_teams_points(team_two, team_one)
                    challenge_object.status = "finished"

        challenge_object.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ReportChallengeProofView(DetailView):
    model = Challenge

    def post(self, request, *args, **kwargs):
        challenge_object = self.get_object()
        proof_first_team = request.POST.get('proof_first_team', None)
        proof_second_team = request.POST.get('proof_second_team', None)
        if proof_first_team:
            challenge_object.proof_first_team = proof_first_team
        if proof_second_team:
            challenge_object.proof_second_team = proof_second_team
        challenge_object.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FixDisputeView(UpdateView):
    model = Challenge

    def post(self, request, *args, **kwargs):
        challenge_object = self.get_object()
        result = request.POST.get('result', None)
        team_one = Team.objects.get(pk=challenge_object.first_team.pk)
        team_two = Team.objects.get(pk=challenge_object.second_team.pk)
        if result == 'first':
            challenge_object.result_first_team = "won"
            challenge_object.result_second_team = "loss"
            update_teams_points(team_one, team_two)
        elif result == 'second':
            challenge_object.result_first_team = "loss"
            challenge_object.result_second_team = "won"
            update_teams_points(team_two, team_one)
        challenge_object.status = 'finished'
        challenge_object.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        user = self.request.user
        object_data = model_to_dict(team)
        context['edit_team_form'] = AddTeamForm(initial=object_data)
        context['invite_form'] = InviteForm()
        members = Membership.objects.filter(team=team, is_invited=False)
        context['members'] = members
        membership = team.participant_team.filter(user=user).first()
        context['is_owner_or_captain'] = membership.is_owner or membership.is_captain if membership else False
        challenges = Challenge.objects.filter(Q(first_team=team.pk) | Q(second_team=team.pk))
        context['challenges'] = challenges
        return context


class KickFromTheTeamView(View):

    def post(self, *args, **kwargs):
        user = get_object_or_404(Account, pk=kwargs['pk'])
        team = Team.objects.get(members=user, is_deleted=False)
        membership = Membership.objects.filter(user=user, team=team, is_invited=False)
        if team.members.count() > 1:
            membership.delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class DisbandTeam(View):
    def post(self, *args, **kwargs):
        team = get_object_or_404(Team, pk=kwargs['pk'])
        membership = Membership(team=team, user=self.request.user, is_owner=True)
        if membership:
            team.is_deleted = True
            team.save()
        return redirect('ladders')


class LeaveFromTeam(View):
    def post(self, *args, **kwargs):
        user = get_object_or_404(Account, pk=kwargs['pk'])
        membership = Membership.objects.filter(user=user, is_invited=False, is_owner=False)
        if membership:
            membership.delete()
        else:
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        return redirect('ladders')


class InviteToTeamView(View):
    def post(self, *args, **kwargs):
        team = get_object_or_404(Team, id=kwargs['pk'])

        if not self.request.user.is_authenticated or not team.members.filter(id=self.request.user.id).exists():
            # messages.error(self.request, 'You are not a member of this team.')
            return redirect('team_detail', pk=team.pk)

        form = InviteForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = Account.objects.filter(username=username).first()

            if user:
                membership = Membership(user=user, team=team, is_invited=True)
                membership.save()
                messages.success(self.request, f'Invitation sent to {user.email}.')
                return redirect('team_detail', pk=team.pk)
            else:
                messages.error(self.request, 'User with this email does not exist.')

        return render(self.request, 'invite.html', {'form': form, 'team': team})


@login_required
def accept_invitation_view(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)

    if not membership.is_invited:
        messages.error(request, 'This invitation is no longer valid.')
        return redirect('team_list')

    if request.method == 'POST':
        membership.is_invited = False
        membership.save()
        messages.success(request, f'You have joined the team {membership.team.name}.')
        return redirect('team_detail', team_id=membership.team.id)

    return render(request, 'accept_invitation.html', {'membership': membership})
