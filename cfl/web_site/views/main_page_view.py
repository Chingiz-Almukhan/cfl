from django.views.generic import TemplateView

from accounts.forms import SignUpForm, LoginForm
from web_site.models import Challenge


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        register_form = SignUpForm()
        login_form = LoginForm()
        challenge = Challenge.objects.all()
        context = {'register_form': register_form, 'login_form': login_form, "challenges": challenge}
        return self.render_to_response(context)
