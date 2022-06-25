from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('auth/', include('rest_auth.urls')),    
    path('auth/register/', include('rest_auth.registration.urls')),
    path('auth/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
