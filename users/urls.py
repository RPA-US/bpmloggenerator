from django.urls import include, path, reverse_lazy, re_path
from django.contrib.auth import views as auth_views
from allauth.account.views import confirm_email

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r'^auth/register/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('auth/register/', include('rest_auth.registration.urls')),
    path('auth/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
