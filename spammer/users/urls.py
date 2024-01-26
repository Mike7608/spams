from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (RegisterView,
                         ProfileView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView,
                         EmailConfirmationFailedView, UserForgotPasswordView, UserPasswordResetConfirmView,
                         UserForgotPasswordNewGenView
                         )

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(template_name='user_form.html'), name='profile'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('password-new-gen/', UserForgotPasswordNewGenView.as_view(), name='password_new_gen'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]
