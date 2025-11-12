from django.urls import path, re_path
from . import views

urlpatterns = [
    # Authentication URLs
    re_path(r'^register/?$', views.RegisterView.as_view(), name='register'),
    re_path(r'^login/?$', views.LoginView.as_view(), name='login'),
    re_path(r'^google-login/?$', views.GoogleLoginView.as_view(), name='google-login'),
    
    # Email verification URLs
    re_path(r'^resend-activation/?$', views.RendActivationView.as_view(), name='resend-activation'),
    re_path(r'^activate-email/?$', views.EmailActivateView.as_view(), name='activate-email'),
    
    # Password management URLs
    re_path(r'^change-password/?$', views.ChangePasswordView.as_view(), name='change-password'),
    re_path(r'^set-password/?$', views.SetPasswordView.as_view(), name='set-password'),
    re_path(r'^password-reset-request/?$', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    re_path(r'^password-reset-confirm/?$', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    re_path(r'^check-email-exists/?$', views.CheckEmailExistsView.as_view(), name='check-email-exists'),

    # User profile URLs
    re_path(r'^profile/?$', views.UpdateUserView.as_view(), name='profile'),
]