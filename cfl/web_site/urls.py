from django.urls import path

from web_site.views.ladder_detail_view import LadderDetailView, MakeTeamView, CreateChallengeView, AcceptChallengeView, \
    DeleteChallenge, ChallengeDetailView, ReportChallengeView, ReportChallengeProofView, FixDisputeView, TeamDetailView, \
    KickFromTheTeamView, DisbandTeam, LeaveFromTeam, InviteToTeamView, accept_invitation_view
from web_site.views.ladders_view import LadderListView, CreateLadderView
from web_site.views.main_page_view import IndexPageView

urlpatterns = [
    path('', IndexPageView.as_view(), name='main'),
    path('ladders', LadderListView.as_view(), name='ladders'),
    path('ladder/<int:pk>', LadderDetailView.as_view(), name='ladder_detail'),
    path('create/ladder', CreateLadderView.as_view(), name='create_ladder'),
    path('create/team/<int:pk>', MakeTeamView.as_view(), name='create_team'),
    path('create/challenge/<int:pk>', CreateChallengeView.as_view(), name='create_challenge'),
    path('accept/challenge/<int:pk>', AcceptChallengeView.as_view(), name='accept_challenge'),
    path('cancel/challenge/<int:pk>', DeleteChallenge.as_view(), name='cancel_challenge'),
    path('challenge/<int:pk>', ChallengeDetailView.as_view(), name='view_challenge'),
    path('report/challenge/<int:pk>', ReportChallengeView.as_view(), name="report_challenge"),
    path('report/proof/<int:pk>', ReportChallengeProofView.as_view(), name="report_proof"),
    path('fix/dispute/challenge/<int:pk>', FixDisputeView.as_view(), name='fix_dispute'),
    path('team/<int:pk>', TeamDetailView.as_view(), name="team_detail"),
    path('kick/player/<int:pk>', KickFromTheTeamView.as_view(), name='kick_from_the_team'),
    path('delete/team/<int:pk>', DisbandTeam.as_view(), name="disband"),
    path('leave/<int:pk>', LeaveFromTeam.as_view(), name='leave'),
    path('teams/<int:pk>/invite/', InviteToTeamView.as_view(), name='team_invite'),
    path('invitations/<int:membership_id>/accept/', accept_invitation_view, name='accept_invitation'),
]
