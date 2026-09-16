from django.urls import path

from .views import (
    csrf_token,
    login_user,
    logout_user,
    me,
    register,
    request_password_reset,
    reset_password,
    users_list,
    verify_password_reset_code,
)


urlpatterns = [
    path('csrf/', csrf_token, name='csrf-token'),
    path('', users_list, name='users-list'),
    path('register/', register, name='user-register'),
    path('login/', login_user, name='user-login'),
    path('logout/', logout_user, name='user-logout'),
    path('me/', me, name='user-me'),
    path('forgot-password/request/', request_password_reset, name='password-reset-request'),
    path('forgot-password/verify/', verify_password_reset_code, name='password-reset-verify'),
    path('forgot-password/reset/', reset_password, name='password-reset'),
]