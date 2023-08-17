from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.tokens import default_token_generator as token_generator

from accounts.forms import LoginForm, SignUpForm, UserChangeForm
from accounts.models import Account
from accounts.utils import send_email_for_verify
from web_site.models import Challenge


# class LoginView(TemplateView):
#     template_name = 'index.html'
#     form = LoginForm
#
#     def post(self, request, *args, **kwargs):
#         form = self.form(request.POST)
#         if not form.is_valid():
#             context = {'login_form': form}
#             return self.render_to_response(context)
#         password = form.cleaned_data.get('password')
#         username = form.cleaned_data.get('username')
#         user = authenticate(request, username=username, password=password)
#         if not user:
#             context = {'login_form': form}
#             return self.render_to_response(context)
#         login(request, user)
#         return redirect('main')
class LogView(LoginView):
    template_name = 'index.html'
    form_class = LoginForm


def logout_view(request):
    logout(request)
    return redirect('login')


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('main')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
        except Exception:
            user = None
        return user


class RegisterView(CreateView):
    template_name = 'index.html'
    form_class = SignUpForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')
            user.save()
            send_email_for_verify(request, user)
            return redirect('confirm_email')
            # login(request, user)
        context = {'register_form': form}
        return self.render_to_response(context)


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile_detail_page.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        object_data = model_to_dict(user)
        context['form'] = UserChangeForm(initial=object_data)
        teams = user.team_members.all()
        challenges = Challenge.objects.filter(Q(first_team__in=teams) | Q(second_team__in=teams))
        challenges = challenges.order_by('-modified')
        context['challenges'] = challenges
        return context

    # def post(self, *args, **kwargs):
    #     form = UserChangeForm(self.request.POST, self.request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
    #     context = {'change_form': form}
    #     return self.render_to_response(context)


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'profile_detail_page.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.pk})
