from django.urls import path

from .views import csrf_token, login_user, logout_user, me, register, users_list


urlpatterns = [
    path('csrf/', csrf_token, name='csrf-token'),
    path('', users_list, name='users-list'),
    path('register/', register, name='user-register'),
    path('login/', login_user, name='user-login'),
    path('logout/', logout_user, name='user-logout'),
    path('me/', me, name='user-me'),
]