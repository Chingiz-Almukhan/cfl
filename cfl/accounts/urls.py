from django.urls import path
from django.views.generic import TemplateView

from accounts.views import RegisterView, logout_view, EmailVerify, LogView, ProfileView, UserChangeView

urlpatterns = [
    path('login', LogView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', logout_view, name='logout'),
    path('invalid_verify/', TemplateView.as_view(template_name='invalid_verify.html'),
         name='invalid_verify'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/', TemplateView.as_view(template_name='confirm_email.html'), name='confirm_email'),
    path('user/<int:pk>', ProfileView.as_view(), name='user_detail'),
    path('edit/<int:pk>', UserChangeView.as_view(), name='change_profile')
]
