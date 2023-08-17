from django.views.generic import ListView, CreateView

from web_site.forms.ladder_form import AddLadderForm
from web_site.models import Ladder


class LadderListView(ListView):
    template_name = 'ladders.html'
    model = Ladder
    context_object_name = 'ladders'

    def get_context_data(self, **kwargs):
        context = super(LadderListView, self).get_context_data(**kwargs)
        context['ladder_form'] = AddLadderForm()
        return context


class CreateLadderView(CreateView):
    template_name = 'ladders.html'
    model = Ladder
    form_class = AddLadderForm
    success_url = '/'

