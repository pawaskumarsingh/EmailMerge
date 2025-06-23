# emails/urls.py
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', custom_login_view, name="login"),
    path('accounts/sign-up/', SignUpView.as_view(), name="signup"),
    path('logout/', Logout, name="logout"),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='account/reset_user_password.html', email_template_name='account/password_reset_email.html'), name='password_reset'),
    # path(r'^reset-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', ResetPasswordView.as_view(), name="reset_password"),
    # path('user-new-password', CreateNewPasswordView.as_view(), name="create_user_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/forget_password.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), name='password_reset_complete'),
]