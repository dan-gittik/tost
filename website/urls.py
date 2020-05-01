from django.urls import path

from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('account', views.account, name='account'),
    path('logout', views.logout, name='logout'),
    path('delete-account', views.delete_account, name='delete-account'),
    path('validate-email', views.validate_email, name='validate-email'),
    path('change-password', views.change_password, name='change-password'),
    path('', views.index, name='index'),
]
