from django.urls import path

from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('account', views.account, name='account'),
    path('logout', views.logout, name='logout'),
    path('', views.index, name='index'),
]
